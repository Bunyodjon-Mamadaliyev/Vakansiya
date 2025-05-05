from django.contrib import admin
from django.utils.html import format_html
from .models import JobSeeker


@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'user', 'location', 'education_level',
        'experience_years', 'date_of_birth', 'phone_number'
    )
    list_filter = ('education_level', 'location', 'experience_years')
    search_fields = (
        'first_name', 'last_name', 'user__username', 'location', 'skills__name'
    )
    filter_horizontal = ('skills',)
    readonly_fields = ('profile_picture_preview',)
    ordering = ('-experience_years', 'last_name')

    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def full_name(self, obj):
        return obj.full_name

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit:cover;" />',
                obj.profile_picture.url
            )
        return "(No image)"

    profile_picture_preview.short_description = 'Profile Picture'
