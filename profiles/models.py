from django.db import models
from django.conf import settings
from skill.models import Skill  # Skill modeli mavjud deb faraz qilamiz


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, blank=True)

    # ... boshqa maydonlar

    def __str__(self):
        return f"{self.user.email} profili"