from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from notification.models import Notification

User = get_user_model()

class NotificationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password='password123'
        )

    def test_create_notification_successfully(self):
        notification = Notification.objects.create(
            user=self.user,
            message='Your job application has been updated.',
            notification_type='job_application'
        )
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, 'Your job application has been updated.')
        self.assertEqual(notification.notification_type, 'job_application')
        self.assertFalse(notification.is_read)

    def test_str_method(self):
        notification = Notification.objects.create(
            user=self.user,
            message='Your job application has been updated.',
            notification_type='job_application'
        )
        self.assertEqual(str(notification), 'Job Application Update for user1')

    def test_is_recent_property(self):
        notification_recent = Notification.objects.create(
            user=self.user,
            message='Your job application has been updated.',
            notification_type='job_application',
            created_at=timezone.now() - timezone.timedelta(hours=2)  # 2 soat oldin
        )
        notification_old = Notification.objects.create(
            user=self.user,
            message='Your job application has expired.',
            notification_type='job_application',
            created_at=timezone.now() - timezone.timedelta(days=2)  # 2 kun oldin
        )
        self.assertTrue(notification_recent.is_recent)
        self.assertFalse(notification_old.is_recent)

    def test_mark_as_read_method(self):
        notification = Notification.objects.create(
            user=self.user,
            message='Your job application has been updated.',
            notification_type='job_application'
        )
        self.assertFalse(notification.is_read)
        notification.mark_as_read()
        self.assertTrue(notification.is_read)

    def test_create_notification_class_method(self):
        notification = Notification.create_notification(
            user=self.user,
            message='New job match found!',
            notification_type='new_job_match'
        )
        self.assertEqual(notification.message, 'New job match found!')
        self.assertEqual(notification.notification_type, 'new_job_match')
        self.assertEqual(notification.user, self.user)
        self.assertFalse(notification.is_read)
