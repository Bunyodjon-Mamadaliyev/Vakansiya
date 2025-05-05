from django.test import TestCase
from django.core.exceptions import ValidationError
from skill.models import Skill
from jobseeker.models import JobSeeker
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

class JobSeekerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='jobseeker1',
            password='password123',
            user_type='job_seeker',
            first_name='Ali',
            last_name='Valiyev'
        )
        self.skill1 = Skill.objects.create(name='Python')
        self.skill2 = Skill.objects.create(name='Django')

    def test_create_job_seeker_successfully(self):
        job_seeker = JobSeeker.objects.create(
            user=self.user,
            first_name='Ali',
            last_name='Valiyev',
            date_of_birth=datetime.date(1990, 1, 1),
            phone_number='998901234567',
            location='Tashkent',
            education_level='bachelor',
            experience_years=5
        )
        self.assertEqual(job_seeker.first_name, 'Ali')
        self.assertEqual(job_seeker.last_name, 'Valiyev')
        self.assertEqual(job_seeker.experience_years, 5)
        self.assertEqual(job_seeker.education_level, 'bachelor')

    def test_str_method(self):
        job_seeker = JobSeeker.objects.create(
            user=self.user,
            first_name='Ali',
            last_name='Valiyev',
            date_of_birth=datetime.date(1990, 1, 1),
            phone_number='998901234567',
            location='Tashkent',
            education_level='bachelor',
            experience_years=5
        )
        self.assertEqual(str(job_seeker), 'Ali Valiyev')

    def test_full_name_property(self):
        job_seeker = JobSeeker.objects.create(
            user=self.user,
            first_name='Ali',
            last_name='Valiyev',
            date_of_birth=datetime.date(1990, 1, 1),
            phone_number='998901234567',
            location='Tashkent',
            education_level='bachelor',
            experience_years=5
        )
        self.assertEqual(job_seeker.full_name, 'Ali Valiyev')

    def test_age_method(self):
        date_of_birth = datetime.date(1990, 1, 1)
        job_seeker = JobSeeker.objects.create(
            user=self.user,
            first_name='Ali',
            last_name='Valiyev',
            date_of_birth=date_of_birth,
            phone_number='998901234567',
            location='Tashkent',
            education_level='bachelor',
            experience_years=5
        )

        today = datetime.date.today()
        expected_age = today.year - date_of_birth.year - (
                (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
        )

        self.assertEqual(job_seeker.age(), expected_age)

    def test_experience_years_validation(self):
        job_seeker = JobSeeker(
            user=self.user,
            first_name='Ali',
            last_name='Valiyev',
            date_of_birth=datetime.date(1990, 1, 1),
            phone_number='998901234567',
            location='Tashkent',
            education_level='bachelor',
            experience_years=60
        )
        with self.assertRaises(ValidationError):
            job_seeker.full_clean()
