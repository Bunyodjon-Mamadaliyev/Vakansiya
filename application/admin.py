from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_seeker', 'job_posting', 'status', 'applied_date', 'updated_date')
    list_filter = ('status', 'applied_date', 'updated_date')
    search_fields = ('job_seeker__user__username', 'job_posting__title')
    readonly_fields = ('applied_date', 'updated_date')
    ordering = ('-applied_date',)

