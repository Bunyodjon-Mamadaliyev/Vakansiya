from django.db import models
from django.conf import settings


class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='employer_profile', limit_choices_to={'user_type': 'employer'})
    company = models.ForeignKey('company.Company',
        on_delete=models.SET_NULL, null=True, blank=True, related_name='employers')
    position = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.position})"