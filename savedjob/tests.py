from django.test import TestCase
from django.utils import timezone
from jobseeker.models import JobSeeker
from jobposting.models import JobPosting
from company.models import Company
from django.contrib.auth import get_user_model
from .models import SavedJob
from datetime import timedelta

User = get_user_model()


class SavedJobModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='jobseeker@example.com',
            username='jobseeker',
            password='testpass123',
            user_type='job_seeker'
        )

        self.employer_user = User.objects.create_user(
            email='employer@example.com',
            username='employer',
            password='testpass123',
            user_type='employer'
        )
        self.job_seeker = JobSeeker.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            date_of_birth='1990-01-01',
            phone_number='+1234567890',
            location='New York',
            education_level='bachelor'
        )
        self.company = Company.objects.create(
            user=self.employer_user,
            name='Test Company',
            description='Test description',
            website='https://example.com'
        )
        self.active_job = JobPosting.objects.create(
            company=self.company,
            title='Active Job',
            description='Active job description',
            requirements='Requirements',
            location='Remote',
            salary_min=50000,
            salary_max=70000,
            is_active=True,
            deadline=timezone.now().date() + timedelta(days=30)
        )
        self.expired_job = JobPosting.objects.create(
            company=self.company,
            title='Expired Job',
            description='Expired job description',
            requirements='Requirements',
            location='Remote',
            salary_min=50000,
            salary_max=70000,
            is_active=True,
            deadline=timezone.now().date() - timedelta(days=1)
        )
        self.inactive_job = JobPosting.objects.create(
            company=self.company,
            title='Inactive Job',
            description='Inactive job description',
            requirements='Requirements',
            location='Remote',
            salary_min=50000,
            salary_max=70000,
            is_active=False,
            deadline=timezone.now().date() + timedelta(days=30)
        )

    def test_create_saved_job(self):
        saved_job = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.active_job
        )

        self.assertEqual(saved_job.job_seeker, self.job_seeker)
        self.assertEqual(saved_job.job_posting, self.active_job)
        self.assertIsNotNone(saved_job.saved_date)
        self.assertTrue(timezone.now() - saved_job.saved_date < timedelta(seconds=1))

    def test_unique_together_constraint(self):
        SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.active_job
        )

        with self.assertRaises(Exception):
            SavedJob.objects.create(
                job_seeker=self.job_seeker,
                job_posting=self.active_job
            )

    def test_saved_date_auto_set(self):
        before_create = timezone.now()
        saved_job = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.active_job
        )
        after_create = timezone.now()

        self.assertTrue(before_create <= saved_job.saved_date <= after_create)

    def test_is_job_active_property(self):
        saved_active = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.active_job
        )
        saved_expired = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.expired_job
        )
        saved_inactive = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.inactive_job
        )

        self.assertTrue(saved_active.is_job_active)
        self.assertFalse(saved_expired.is_job_active)
        self.assertFalse(saved_inactive.is_job_active)

    def test_meta_options(self):
        self.assertEqual(SavedJob._meta.verbose_name, 'Saved Job')
        self.assertEqual(SavedJob._meta.verbose_name_plural, 'Saved Jobs')
        self.assertEqual(SavedJob._meta.ordering, ['-saved_date'])
        self.assertEqual(SavedJob._meta.unique_together, (('job_seeker', 'job_posting'),))

    def test_str_method(self):
        saved_job = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.active_job
        )
        expected_str = f"{self.job_seeker} saved {self.active_job}"
        self.assertEqual(str(saved_job), expected_str)

    def test_ordering(self):
        sj1 = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.active_job,
            saved_date=timezone.now() - timedelta(days=2)
        )
        sj2 = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.expired_job,
            saved_date=timezone.now() - timedelta(days=1)
        )
        sj3 = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.inactive_job,
            saved_date=timezone.now()
        )
        saved_jobs = SavedJob.objects.all()
        self.assertEqual(saved_jobs[0].id, sj3.id)
        self.assertEqual(saved_jobs[1].id, sj2.id)
        self.assertEqual(saved_jobs[2].id, sj1.id)

    def test_related_names(self):
        saved_job = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.active_job
        )
        self.assertIn(saved_job, self.job_seeker.saved_jobs.all())
        self.assertIn(saved_job, self.active_job.saved_by.all())
