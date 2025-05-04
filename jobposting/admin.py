from django.contrib import admin
from .models import JobPosting

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'company', 'job_type', 'experience_level', 'education_required',
        'location', 'salary_range', 'is_active', 'is_expired', 'posted_date', 'deadline', 'views_count'
    )
    list_filter = (
        'job_type', 'experience_level', 'education_required', 'is_active', 'company', 'location', 'deadline'
    )
    search_fields = ('title', 'company__name', 'location', 'skills_required__name')
    filter_horizontal = ('skills_required',)
    readonly_fields = ('posted_date', 'views_count')
    ordering = ('-posted_date',)

    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.admin_order_field = 'deadline'
