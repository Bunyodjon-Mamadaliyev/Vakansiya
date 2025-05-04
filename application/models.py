from django.db import models
from django.utils import timezone

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('offered', 'Offered'),
        ('hired', 'Hired'),
    ]
    job_posting = models.ForeignKey('jobposting.JobPosting', on_delete=models.CASCADE, related_name='applications')
    job_seeker = models.ForeignKey('jobseeker.JobSeeker', on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='application_resumes/', null=True, blank=True)
    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job_posting', 'job_seeker')
        ordering = ['-applied_date']
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'

    def __str__(self):
        return f"{self.job_seeker} - {self.job_posting} ({self.status})"

    def save(self, *args, **kwargs):
        self.updated_date = timezone.now()
        super().save(*args, **kwargs)