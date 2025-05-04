from django.db import models
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('job_application', 'Job Application Update'),
        ('new_job_match', 'New Job Match'),
        ('message', 'Message'),
        ('profile_view', 'Profile View'),
        ('job_expiring', 'Job Expiring Soon'),
        ('application_deadline', 'Application Deadline'),
        ('system_alert', 'System Alert'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                             related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    related_object_id = models.PositiveIntegerField( null=True, blank=True,
                        help_text="ID of the related object (JobPosting, Application, etc.)")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [models.Index(fields=['user', 'is_read']),]

    def __str__(self):
        return f"{self.get_notification_type_display()} for {self.user}"

    @property
    def is_recent(self):
        return (timezone.now() - self.created_at).days < 1

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

    @classmethod
    def create_notification(cls, user, message, notification_type, related_object_id=None):
        return cls.objects.create( user=user, message=message, notification_type=notification_type,
                                   related_object_id=related_object_id)