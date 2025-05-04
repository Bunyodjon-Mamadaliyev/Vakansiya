from django.contrib import admin
from .models import Employer

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company', 'position', 'is_primary')
    list_filter = ('is_primary', 'company')
    search_fields = ('user__email', 'position', 'company__name')
    autocomplete_fields = ['user', 'company']
