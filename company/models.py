from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Company(models.Model):
    INDUSTRY_CHOICES = [
        ('it', 'Information Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail'),
        ('construction', 'Construction'),
        ('transportation', 'Transportation'),
        ('hospitality', 'Hospitality'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                    limit_choices_to={'user_type': 'employer'}, related_name='company')
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    location = models.CharField(max_length=100)
    founded_year = models.IntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(2023)],
        null=True, blank=True
    )
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    employees_count = models.IntegerField(default=0, validators=[MinValueValidator(1)], null=True, blank=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name