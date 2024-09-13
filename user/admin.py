from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import NewUser, OTP, Contact


class UserAdminConfig(BaseUserAdmin):
    ordering = ['-date_joined']
    list_display = ['username', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'is_superuser']
    list_editable = ['is_active']
    search_fields = ['username', 'first_name', 'last_name', 'phone_number']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']

    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')
        }),
    )
    readonly_fields = ['date_joined', 'last_login']


admin.site.register(NewUser, UserAdminConfig)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['user__username', 'otp_code']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'contact_date']