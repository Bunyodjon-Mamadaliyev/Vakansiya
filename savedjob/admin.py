from django.contrib import admin
from .models import SavedJob

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'job_seeker', 'job_posting', 'saved_date', 'is_job_active'
    )
    list_filter = ('saved_date',)
    search_fields = (
        'job_seeker__first_name', 'job_seeker__last_name',
        'job_posting__title', 'job_posting__company__name'
    )
    ordering = ('-saved_date',)
    readonly_fields = ('saved_date',)

    def is_job_active(self, obj):
        return obj.is_job_active
    is_job_active.boolean = True
    is_job_active.short_description = 'Job Active?'
