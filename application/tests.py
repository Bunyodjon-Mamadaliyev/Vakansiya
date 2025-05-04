from django.test import TestCase
from django.utils import timezone
from application.models import JobApplication
from jobposting.models import JobPosting
from jobseeker.models import JobSeeker
from django.contrib.auth import get_user_model

User = get_user_model()

class JobApplicationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.job_seeker = JobSeeker.objects.create(user=self.user, first_name='John', last_name='Doe')
        self.job_posting = JobPosting.objects.create(
            title='Backend Developer',
            description='Django developer needed.',
            location='Tashkent',
            company_name='Tech Corp',
            posted_date=timezone.now()
        )

    def test_create_job_application(self):
        application = JobApplication.objects.create(
            job_posting=self.job_posting,
            job_seeker=self.job_seeker,
            cover_letter='I am very interested in this position.'
        )
        self.assertEqual(application.status, 'applied')
        self.assertIsNotNone(application.applied_date)
        self.assertIsNone(application.resume)

    def test_unique_together_constraint(self):
        JobApplication.objects.create(
            job_posting=self.job_posting,
            job_seeker=self.job_seeker,
            cover_letter='My first application.'
        )
        with self.assertRaises(Exception):
            JobApplication.objects.create(
                job_posting=self.job_posting,
                job_seeker=self.job_seeker,
                cover_letter='Duplicate application.'
            )

    def test_str_method(self):
        application = JobApplication.objects.create(
            job_posting=self.job_posting,
            job_seeker=self.job_seeker,
            cover_letter='This is my application.'
        )
        expected_str = f"{self.job_seeker} - {self.job_posting} ({application.status})"
        self.assertEqual(str(application), expected_str)

    def test_updated_date_changes_on_save(self):
        application = JobApplication.objects.create(
            job_posting=self.job_posting,
            job_seeker=self.job_seeker,
            cover_letter='Initial letter.'
        )
        original_updated_date = application.updated_date
        application.cover_letter = 'Updated letter.'
        application.save()
        self.assertNotEqual(application.updated_date, original_updated_date)
