from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Notification
from datetime import timedelta

User = get_user_model()

class NotificationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.notification_data = {
            'user': self.user,
            'message': 'Test notification message',
            'notification_type': 'message',
        }

    def test_create_notification(self):
        notification = Notification.objects.create(**self.notification_data)
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, self.notification_data['message'])
        self.assertEqual(notification.notification_type, self.notification_data['notification_type'])
        self.assertFalse(notification.is_read)
        self.assertIsNotNone(notification.created_at)
        self.assertIsNone(notification.related_object_id)

    def test_notification_str(self):
        notification = Notification.objects.create(**self.notification_data)
        expected_str = f"{notification.get_notification_type_display()} for {self.user}"
        self.assertEqual(str(notification), expected_str)

    def test_is_recent_property(self):
        recent_notification = Notification.objects.create(**self.notification_data)
        self.assertTrue(recent_notification.is_recent)
        old_notification = Notification.objects.create(**self.notification_data)
        old_notification.created_at = timezone.now() - timedelta(days=2)
        old_notification.save()
        self.assertFalse(old_notification.is_recent)

    def test_mark_as_read(self):
        notification = Notification.objects.create(**self.notification_data)
        self.assertFalse(notification.is_read)
        notification.mark_as_read()
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
        notification.mark_as_read()
        self.assertTrue(notification.is_read)

    def test_create_notification_classmethod(self):
        message = "Test class method notification"
        notification = Notification.create_notification(
            user=self.user,
            message=message,
            notification_type='job_application',
            related_object_id=1
        )

        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.notification_type, 'job_application')
        self.assertEqual(notification.related_object_id, 1)

    def test_notification_types(self):
        for type_code, _ in Notification.NOTIFICATION_TYPES:
            notification = Notification.objects.create(
                user=self.user,
                message=f"{type_code} notification",
                notification_type=type_code
            )
            notification.full_clean()

    def test_meta_options(self):
        self.assertEqual(Notification._meta.ordering, ['-created_at'])
        self.assertEqual(Notification._meta.verbose_name, 'Notification')
        self.assertEqual(Notification._meta.verbose_name_plural, 'Notifications')
        self.assertEqual(len(Notification._meta.indexes), 1)

    def test_related_object_id_optional(self):
        notification1 = Notification.objects.create(**self.notification_data)
        self.assertIsNone(notification1.related_object_id)
        notification_data_with_id = {**self.notification_data, 'related_object_id': 123}
        notification2 = Notification.objects.create(**notification_data_with_id)
        self.assertEqual(notification2.related_object_id, 123)

    def test_notification_ordering(self):
        notification1 = Notification.objects.create(**self.notification_data)
        notification2 = Notification.objects.create(**self.notification_data)
        notification3 = Notification.objects.create(**self.notification_data)
        notification1.created_at = timezone.now() - timedelta(hours=2)
        notification1.save()
        notification2.created_at = timezone.now() - timedelta(hours=1)
        notification2.save()
        notifications = Notification.objects.all()
        self.assertEqual(notifications[0].id, notification3.id)
        self.assertEqual(notifications[1].id, notification2.id)
        self.assertEqual(notifications[2].id, notification1.id)