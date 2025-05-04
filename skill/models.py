# models.py
from django.db import models
from django.core.exceptions import ValidationError


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('soft', 'Soft Skills'),
        ('language', 'Language'),
        ('tool', 'Tools & Technologies'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='technical')

    def clean(self):
        if self.category not in dict(self.CATEGORY_CHOICES).keys():
            raise ValidationError({'category': 'Noto\'g\'ri kategoriya tanlandi'})

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Skills'