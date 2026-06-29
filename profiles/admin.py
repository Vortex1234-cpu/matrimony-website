from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, PartnerPreference, ProfilePhoto


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'user', 'age',
        'city', 'religion', 'is_approved',
        'is_premium', 'created_at'
    ]
    list_filter = [
        'is_approved', 'is_premium',
        'religion', 'gender'
    ]
    search_fields = [
        'full_name', 'city', 'district',
        'religion', 'caste'
    ]
    list_editable = ['is_approved']
    ordering = ['-created_at']

    def gender_display(self, obj):
        return obj.user.gender
    gender_display.short_description = 'Gender'

    def photo_preview(self, obj):
        if obj.profile_photo:
            try:
                return format_html(
                    '<img src="{}" width="50" '
                    'height="50" style="border-radius:50%;'
                    'object-fit:cover;" '
                    'onerror="this.src=\'\';'
                    'this.alt=\'No photo\'"/>',
                    obj.profile_photo.url
                )
            except Exception:
                return '👤'
        return '👤'
    photo_preview.short_description = 'Photo'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(PartnerPreference)
admin.site.register(ProfilePhoto)