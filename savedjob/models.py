from django.db import models
from django.utils import timezone

class SavedJob(models.Model):
    job_seeker = models.ForeignKey('jobseeker.JobSeeker', on_delete=models.CASCADE,
                                   related_name='saved_jobs')
    job_posting = models.ForeignKey('jobposting.JobPosting', on_delete=models.CASCADE,
                                    related_name='saved_by')
    saved_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('job_seeker', 'job_posting')
        ordering = ['-saved_date']
        verbose_name = 'Saved Job'
        verbose_name_plural = 'Saved Jobs'

    def __str__(self):
        return f"{self.job_seeker} saved {self.job_posting}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.saved_date = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_job_active(self):
        return self.job_posting.is_active and not self.job_posting.is_expired