from django.test import TestCase
from django.utils import timezone
from jobseeker.models import JobSeeker
from jobposting.models import JobPosting
from .models import SavedJob

class SavedJobModelTest(TestCase):

    def setUp(self):
        # Create a JobSeeker
        self.job_seeker = JobSeeker.objects.create(
            first_name="John", last_name="Doe", date_of_birth="1990-01-01",
            phone_number="1234567890", location="New York",
            education_level="bachelor"
        )

        # Create a JobPosting
        self.job_posting = JobPosting.objects.create(
            company=self.job_seeker.user.company,
            title="Software Developer",
            description="Develop software.",
            requirements="Python, Django",
            responsibilities="Develop and maintain web applications",
            location="New York",
            job_type="full_time",
            experience_level="mid",
            education_required="bachelor",
            salary_min=50000,
            salary_max=80000,
            deadline="2025-01-01",
            views_count=0
        )

    def test_create_saved_job_successfully(self):
        saved_job = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.job_posting
        )
        self.assertEqual(saved_job.job_seeker, self.job_seeker)
        self.assertEqual(saved_job.job_posting, self.job_posting)
        self.assertIsNotNone(saved_job.saved_date)

    def test_str_method(self):
        saved_job = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.job_posting
        )
        self.assertEqual(str(saved_job), f"{self.job_seeker} saved {self.job_posting}")

    def test_is_job_active_property(self):
        # Active job and not expired
        saved_job = SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.job_posting
        )
        self.assertTrue(saved_job.is_job_active)

        # Inactive job (expired job)
        self.job_posting.is_active = False
        self.job_posting.save()
        self.assertFalse(saved_job.is_job_active)

        # Active but expired job
        self.job_posting.is_active = True
        self.job_posting.deadline = timezone.now() - timezone.timedelta(days=1)
        self.job_posting.save()
        self.assertFalse(saved_job.is_job_active)

    def test_unique_constraint(self):
        # Save job once
        SavedJob.objects.create(
            job_seeker=self.job_seeker,
            job_posting=self.job_posting
        )

        # Try to save the same job again (this should raise an IntegrityError)
        with self.assertRaises(Exception):
            SavedJob.objects.create(
                job_seeker=self.job_seeker,
                job_posting=self.job_posting
            )
