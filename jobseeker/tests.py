from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from skill.models import Skill
from jobseeker.models import JobSeeker
from django.contrib.auth import get_user_model

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
            date_of_birth='1990-05-01',
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
            date_of_birth='1990-05-01',
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
            date_of_birth='1990-05-01',
            phone_number='998901234567',
            location='Tashkent',
            education_level='bachelor',
            experience_years=5
        )
        self.assertEqual(job_seeker.full_name, 'Ali Valiyev')

    def test_age_method(self):
        job_seeker = JobSeeker.objects.create(
            user=self.user,
            first_name='Ali',
            last_name='Valiyev',
            date_of_birth='1990-05-01',
            phone_number='998901234567',
            location='Tashkent',
            education_level='bachelor',
            experience_years=5
        )
        self.assertEqual(job_seeker.age(), 34)  # 2024-1990 = 34

    def test_experience_years_validation(self):
        job_seeker = JobSeeker(
            user=self.user,
            first_name='Ali',
            last_name='Valiyev',
            date_of_birth='1990-05-01',
            phone_number='998901234567',
            location='Tashkent',
            education_level='bachelor',
            experience_years=60  # Noto‘g‘ri qiymat, 60+ yillik tajriba noto‘g‘ri
        )
        with self.assertRaises(ValidationError):
            job_seeker.full_clean()
