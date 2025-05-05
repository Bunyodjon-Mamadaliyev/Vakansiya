from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'user_type': 'job_seeker',
        }

    def test_create_user(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.user_type, self.user_data['user_type'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNotNone(user.date_joined)

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123',
            user_type='admin',
        )

        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertEqual(superuser.username, 'admin')
        self.assertEqual(superuser.user_type, 'admin')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_email_unique(self):
        CustomUser.objects.create_user(**self.user_data)

        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                email='test@example.com',
                username='differentuser',
                password='testpass123',
                user_type='employer',
            )

    def test_user_type_choices(self):
        valid_user = CustomUser.objects.create_user(**self.user_data)
        valid_user.full_clean()

        invalid_user = CustomUser(
            email='invalid@example.com',
            username='invaliduser',
            password='testpass123',
            user_type='invalid_type',
        )

        with self.assertRaises(ValidationError):
            invalid_user.full_clean()

    def test_required_fields(self):
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(
                email='missingusername@example.com',
                password='testpass123',
                user_type='job_seeker',
            )

    def test_jobseeker_property(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertIsNone(user.jobseeker)
        from unittest.mock import Mock
        mock_jobseeker = Mock()
        user._jobseeker = mock_jobseeker
        self.assertEqual(user.jobseeker, mock_jobseeker)

    def test_employer_property(self):
        employer_user = CustomUser.objects.create_user(
            email='employer@example.com',
            username='employer',
            password='testpass123',
            user_type='employer',
        )
        self.assertIsNone(employer_user.employer)
        from unittest.mock import Mock
        mock_employer = Mock()
        employer_user._employer = mock_employer
        self.assertEqual(employer_user.employer, mock_employer)

    def test_str_method(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])

    def test_email_field_attribute(self):
        self.assertEqual(CustomUser.EMAIL_FIELD, 'email')

    def test_username_field_attribute(self):
        self.assertEqual(CustomUser.USERNAME_FIELD, 'email')

    def test_required_fields_attribute(self):
        self.assertEqual(CustomUser.REQUIRED_FIELDS, ['username'])