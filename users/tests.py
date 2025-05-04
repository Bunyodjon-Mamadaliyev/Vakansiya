from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # To ensure 'username' is still required when creating a user

    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=10,
        choices=[('employer', 'Employer'), ('job_seeker', 'Job Seeker'), ('admin', 'Admin')],
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

    def clean(self):
        """Custom validation for user type"""
        if self.user_type == 'job_seeker' and hasattr(self, 'jobseeker') and not self.jobseeker:
            raise ValidationError('A Job Seeker profile must be created for users with user_type "job_seeker".')
        elif self.user_type == 'employer' and hasattr(self, 'employer') and not self.employer:
            raise ValidationError('An Employer profile must be created for users with user_type "employer".')

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
