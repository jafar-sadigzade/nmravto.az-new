import random
from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Username daxil etməlisiniz!'))
        if not phone_number:
            raise ValueError(_('Telefon nömrəsi daxil etməlisiniz!'))

        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superistifadəçi üçün is_staff aktiv olmalıdır!'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superistifadəçi üçün is_superuser aktiv olmalıdır!'))

        return self.create_user(username, phone_number, password, **extra_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=50, unique=True)
    first_name = models.CharField(_('Adınız'), max_length=50, blank=True)
    last_name = models.CharField(_('Soyadınız'), max_length=50, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=_("Telefon nömrəsi +999999999 formatında olmalıdır."))
    phone_number = models.CharField(_('Telefon nömrəsi'), validators=[phone_regex], max_length=17,
                                    blank=True)
    date_joined = models.DateTimeField(_("Qoşulma tarixi"), default=timezone.now)
    is_staff = models.BooleanField(_("İşçi statusu"), default=False)
    is_active = models.BooleanField(_("Hesab aktivlik statusu"), default=True)

    objects = CustomManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    class Meta:
        verbose_name = 'Yeni istifadəçi'
        verbose_name_plural = 'Yeni istifadəçi'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(_('OTP'), max_length=6)
    created_at = models.DateTimeField(_('Yaradılma tarixi'), auto_now_add=True)
    is_active = models.BooleanField(_('Aktivlik'), default=True)

    # attempt = models.positiveintegerfield(max=3)

    def generate_otp(self):
        if self.daily_attempts() > 3:
            self.delete()
            raise ValueError(_("Bu günlük OTP limitiniz bitmişdir!"))
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.created_at = timezone.now()
        self.is_active = True
        # self.attempt+=1
        self.save()
        return self.otp_code

    def validate_otp(self, otp_code):
        if self.is_active and self.otp_code == otp_code and timezone.now() <= self.created_at + timedelta(minutes=3):
            self.is_active = False
            self.save()
            return True
        return False

    def daily_attempts(self):  # @property self.daily_attempts
        today = timezone.now().date()
        return OTP.objects.filter(user=self.user, created_at__date=today).count()

    def __str__(self):
        return f"OTP for {self.user.username} - {self.otp_code}"

    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'


class Contact(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    contact_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        ordering = ("-contact_date",)
        verbose_name = 'Əlaqə'
        verbose_name_plural = 'Əlaqə'
