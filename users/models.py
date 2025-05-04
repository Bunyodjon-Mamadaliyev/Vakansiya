from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=10,
        choices=[
            ('employer', 'Employer'),
            ('job_seeker', 'Job Seeker'),
            ('admin', 'Admin'),
        ],
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    @property
    def jobseeker(self):
        """Returns the related job seeker profile if exists"""
        if hasattr(self, '_jobseeker'):
            return self._jobseeker
        from jobseeker.models import JobSeeker
        self._jobseeker = JobSeeker.objects.filter(user=self).first()
        return self._jobseeker

    @property
    def employer(self):
        """Returns the related employer profile if exists"""
        if hasattr(self, '_employer'):
            return self._employer
        from employer.models import Employer
        self._employer = Employer.objects.filter(user=self).first()
        return self._employer
