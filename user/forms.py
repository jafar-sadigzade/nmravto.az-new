from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext as _

from user.models import NewUser, Contact

User = get_user_model()


class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=17,
        validators=[NewUser.phone_regex],
        help_text="Telefon nömrəsi +999999999 formatında olmalıdır."
    )

    class Meta:
        model = NewUser
        fields = ('username', 'phone_number', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class OTPForm(forms.Form):
    otp_code = forms.CharField(max_length=6)


class PasswordResetForm(forms.Form):
    phone_number = forms.CharField(
        max_length=17,
        validators=[NewUser.phone_regex],
        help_text="Telefon nömrəsi +999999999 formatında olmalıdır."
    )


class SetPasswordForm(forms.Form):
    otp_code = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Parollar eyni deyil!")


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['title', 'content']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': _('İstifadəçi adı'),
            'first_name': _('Adınız'),
            'last_name': _('Soyadınız'),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_('Bu istifadəçi adı artıq mövcuddur. Başqa bir istifadəçi adı seçin.'))
        return username
