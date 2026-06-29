from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 'first_name', 'phone',
        'email', 'gender', 'is_verified',
        'is_staff', 'date_joined'
    ]
    list_filter = [
        'is_staff', 'is_superuser',
        'is_verified', 'gender'
    ]
    search_fields = [
        'username', 'first_name',
        'phone', 'email'
    ]
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {
            'fields': (
                'phone', 'gender',
                'is_verified', 'is_profile_complete',
                'otp_code', 'otp_created_at'
            )
        }),
    )


admin.site.register(User, CustomUserAdmin)