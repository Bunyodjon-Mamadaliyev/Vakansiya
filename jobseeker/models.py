from django.db import models
from django.conf import settings
from skill.models import Skill
from django.core.validators import MinValueValidator, MaxValueValidator

class JobSeeker(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('high_school', 'High School'),
        ('vocational', 'Vocational School'),
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('phd', 'PhD'),
        ('other', 'Other'),
    ]
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                limit_choices_to={'user_type': 'job_seeker'}, related_name='job_seeker')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    experience_years = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)], default=0)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    class Meta:
        ordering = ['-experience_years', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def age(self):
        import datetime
        return datetime.date.today().year - self.date_of_birth.year