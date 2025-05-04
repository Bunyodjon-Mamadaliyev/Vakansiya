from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'industry', 'location', 'founded_year', 'employees_count')
    list_filter = ('industry', 'location', 'founded_year')
    search_fields = ('name', 'location', 'user__username')
    ordering = ('name',)
