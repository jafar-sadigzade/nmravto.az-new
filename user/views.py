from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views import View

from user.forms import RegisterForm, LoginForm, OTPForm, PasswordResetForm, SetPasswordForm, ContactForm, ProfileForm
from user.models import NewUser, OTP

User = get_user_model()


class LoginRequestView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "username və ya password səhvdir!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('register')))
        return render(request, 'login.html', {'form': form})


class LogoutRequestView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class RegisterRequestView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "register.html", {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                otp_instance = OTP.objects.create(user=user)
                otp_code = otp_instance.generate_otp()
                # Uncomment to send OTP via WHATSAPP
                # send_otp(user.phone_number, otp_code)
                messages.success(self.request,
                                 "Qeydiyyatınız uğurla tamamlandı! Hesabı aktivləşdirmək üçün bir dəfəlik parolu daxil edin!")
                return redirect('validate_otp_view', username=user.username, phone_number=user.phone_number)
            except ValueError as e:
                messages.error(self.request, str(e))
        return render(request, "register.html", {'form': form})


class ValidateOtpView(View):
    def get_user(self, username, phone_number):
        return get_object_or_404(NewUser, username=username, phone_number=phone_number)

    def get(self, request, username, phone_number):
        user = self.get_user(username, phone_number)
        otp_instance = OTP.objects.filter(user=user, is_active=True).latest('created_at')
        otp_expiration_time = otp_instance.created_at + timedelta(minutes=3)
        otp_attempts = OTP.objects.filter(user=user, created_at__date=timezone.now().date()).count()
        show_timer = otp_attempts <= 3
        form = OTPForm()

        return render(request, 'otp.html', {
            'form': form,
            'username': username,
            'phone_number': phone_number,
            'otp_expiration_time': otp_expiration_time,
            'show_timer': show_timer,
        })

    def post(self, request, username, phone_number):
        user = self.get_user(username, phone_number)
        otp_attempts = OTP.objects.filter(user=user, created_at__date=timezone.now().date()).count()
        form = OTPForm(request.POST)

        if 'send_again' in request.POST:
            self.send_new_otp(user, phone_number)
            return redirect('validate_otp_view', username=username, phone_number=phone_number)

        if form.is_valid():
            otp_code = form.cleaned_data.get('otp_code')
            otp_instance = OTP.objects.filter(user=user, is_active=True).latest('created_at')

            if otp_instance.validate_otp(otp_code):
                user.is_active = True
                user.save()
                messages.success(self.request, "OTP təsdiqləndi! Hesabınız aktivdir.")
                return redirect('login')
            else:
                messages.error(self.request, "Yanlış və ya müddəti bitmiş OTP.")

        otp_instance = OTP.objects.filter(user=user, is_active=True).latest('created_at')
        otp_expiration_time = otp_instance.created_at + timedelta(minutes=3)
        show_timer = otp_attempts <= 3

        return render(request, 'otp.html', {
            'form': form,
            'username': username,
            'phone_number': phone_number,
            'otp_expiration_time': otp_expiration_time,
            'show_timer': show_timer,
        })

    def send_new_otp(self, user, phone_number):
        try:
            otp_instance = OTP.objects.create(user=user)
            otp_code = otp_instance.generate_otp()
            # Uncomment to send OTP via WHATSAPP
            # send_otp(phone_number, otp_code)
            messages.success(self.request, "Yeni OTP göndərildi!")
        except ValueError as e:
            messages.error(self.request, str(e))


class ForgetPasswordRequestView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'forget-password.html', {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            user = NewUser.objects.filter(phone_number=phone_number).first()

            if user:
                self.send_new_otp(user, phone_number)
                return redirect('reset_password_request', phone_number=phone_number)
            else:
                messages.error(self.request, "Bu telefon nömrəsi ilə qeydiyyat yoxdur.")
                return redirect('forget_password_request')
        return render(request, 'forget-password.html', {'form': form})

    def send_new_otp(self, user, phone_number):
        try:
            otp_instance = OTP.objects.create(user=user)
            otp_code = otp_instance.generate_otp()
            # Uncomment to send OTP via WHATSAPP
            # send_otp(phone_number, otp_code)
            messages.success(self.request, "Bir dəfəlik parol göndərildi! Zəhmət olmasa daxil edin.")
        except ValueError as e:
            messages.error(self.request, str(e))


class ResetPasswordRequestView(View):
    def get_user(self, phone_number):
        return get_object_or_404(NewUser, phone_number=phone_number)

    def get(self, request, phone_number):
        user = self.get_user(phone_number)
        otp_instance = OTP.objects.filter(user=user, is_active=True).latest('created_at')
        otp_expiration_time = otp_instance.created_at + timedelta(minutes=3)
        otp_attempts = OTP.objects.filter(user=user, created_at__date=timezone.now().date()).count()
        show_timer = otp_attempts <= 3
        form = SetPasswordForm()

        return render(request, 'reset-password.html', {
            'form': form,
            'phone_number': phone_number,
            'show_timer': show_timer,
            'otp_expiration_time': otp_expiration_time
        })

    def post(self, request, phone_number):
        user = self.get_user(phone_number)
        otp_attempts = OTP.objects.filter(user=user, created_at__date=timezone.now().date()).count()
        form = SetPasswordForm(request.POST)

        if 'send_again' in request.POST:
            self.send_new_otp(user, phone_number)
            return redirect('reset_password_request', phone_number=phone_number)

        if form.is_valid():
            otp_code = form.cleaned_data.get('otp_code')
            new_password = form.cleaned_data.get('new_password')
            otp_instance = OTP.objects.filter(user=user, is_active=True).latest('created_at')

            if otp_instance.validate_otp(otp_code):
                user.set_password(new_password)
                user.save()
                messages.success(self.request, "Parolunuz uğurla dəyişdirildi! Zəhmət olmasa daxil olun.")
                return redirect('login')
            else:
                messages.error(self.request, "Yanlış və ya müddəti bitmiş OTP.")

        otp_instance = OTP.objects.filter(user=user, is_active=True).latest('created_at')
        otp_expiration_time = otp_instance.created_at + timedelta(minutes=3)
        show_timer = otp_attempts <= 3

        return render(request, 'reset-password.html', {
            'form': form,
            'phone_number': phone_number,
            'show_timer': show_timer,
            'otp_expiration_time': otp_expiration_time
        })

    def send_new_otp(self, user, phone_number):
        try:
            otp_instance = OTP.objects.create(user=user)
            otp_code = otp_instance.generate_otp()
            # Uncomment to send OTP via WHATSAPP
            # send_otp(phone_number, otp_code)
            messages.success(self.request, "Yeni OTP göndərildi!")
        except ValueError as e:
            messages.error(self.request, str(e))


class ContactCreateView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save(commit=False)

            if request.user.is_authenticated:
                contact.user = request.user
            else:
                # Save the contact without associating with any user
                # For example, you can set user=None or handle it based on your application logic
                contact.user = None

            contact.save()
            messages.success(request, "İstəyiniz uğurla qeydə alındı!")
            return render(request, 'contact.html', {'form': ContactForm()})

        return render(request, 'contact.html', {'form': form})


class ProfileView(View):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        form = ProfileForm(instance=user)
        return render(request, 'profile.html', {'form': form, 'user': user})

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(self.request, _('Profiliniz uğurla yeniləndi.'))
            return redirect('profile')
        else:
            messages.error(self.request, _('Bu istifadəçi adı artıq istifadə olunub!'))  # TODO I know it's a big problem )))
        return render(request, 'profile.html', {'form': form, 'user': user})
