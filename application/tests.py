from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.utils import timezone
from jobposting.models import JobPosting
from jobseeker.models import JobSeeker
from company.models import Company
from django.contrib.auth import get_user_model
from .models import JobApplication
from datetime import timedelta
from django.db import IntegrityError, transaction
import os

User = get_user_model()

class JobApplicationModelTests(TestCase):
    def setUp(self):
        self.employer_user = User.objects.create_user(
            email='employer@example.com',
            username='employer',
            password='testpass123',
            user_type='employer'
        )
        self.job_seeker_user = User.objects.create_user(
            email='jobseeker@example.com',
            username='jobseeker',
            password='testpass123',
            user_type='job_seeker'
        )

        self.company = Company.objects.create(
            user=self.employer_user,
            name='Test Company',
            description='Test description',
            website='https://example.com'
        )

        self.job_posting = JobPosting.objects.create(
            company=self.company,
            title='Software Developer',
            description='Test description',
            requirements='Test requirements',
            location='Remote',
            salary_min=60000,
            salary_max=90000,
            deadline=timezone.now().date() + timedelta(days=30)
        )
        self.job_seeker = JobSeeker.objects.create(
            user=self.job_seeker_user,
            first_name='John',
            last_name='Doe',
            date_of_birth='1990-01-01',
            phone_number='+1234567890',
            location='New York',
            education_level='bachelor'
        )
        self.resume_file = SimpleUploadedFile(
            "test_resume.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        self.application_data = {
            'job_posting': self.job_posting,
            'job_seeker': self.job_seeker,
            'cover_letter': 'I am excited to apply for this position...',
            'status': 'applied'
        }

    def tearDown(self):
        try:
            for application in JobApplication.objects.all():
                if application.resume and os.path.exists(application.resume.path):
                    os.remove(application.resume.path)
        except Exception:
            pass

    def test_create_application(self):
        application = JobApplication.objects.create(**self.application_data)
        self.assertEqual(application.job_posting, self.job_posting)
        self.assertEqual(application.job_seeker, self.job_seeker)
        self.assertEqual(application.cover_letter, 'I am excited to apply for this position...')
        self.assertEqual(application.status, 'applied')
        self.assertIsNotNone(application.applied_date)
        self.assertIsNotNone(application.updated_date)
        self.assertFalse(bool(application.resume))

    def test_create_application_with_resume(self):
        application = JobApplication.objects.create(
            **self.application_data,
            resume=self.resume_file
        )
        self.assertTrue(bool(application.resume))
        self.assertIn('test_resume', application.resume.name)

    def test_unique_together_constraint(self):
        JobApplication.objects.create(**self.application_data)
        with self.assertRaises(IntegrityError):
            try:
                with transaction.atomic():
                    JobApplication.objects.create(**self.application_data)
            except IntegrityError:
                raise

    def test_status_choices(self):
        for status_code, _ in JobApplication.STATUS_CHOICES:
            application = JobApplication(
                **{**self.application_data, 'status': status_code}
            )
            try:
                application.full_clean()
            except ValidationError:
                self.fail(f"Status {status_code} should be valid")

    def test_default_status(self):
        data = {k: v for k, v in self.application_data.items() if k != 'status'}
        application = JobApplication.objects.create(**data)
        self.assertEqual(application.status, 'applied')

    def test_auto_dates(self):
        before_create = timezone.now()
        application = JobApplication.objects.create(**self.application_data)
        after_create = timezone.now()

        self.assertTrue(before_create <= application.applied_date <= after_create)
        self.assertTrue(before_create <= application.updated_date <= after_create)

        old_updated = application.updated_date
        application.cover_letter = "Updated content"
        application.save()
        self.assertGreater(application.updated_date, old_updated)

    def test_ordering(self):
        js2_user = User.objects.create_user(username='js2', email='js2@test.com', password='pass',
                                            user_type='job_seeker')
        js3_user = User.objects.create_user(username='js3', email='js3@test.com', password='pass',
                                            user_type='job_seeker')
        js2 = JobSeeker.objects.create(user=js2_user, first_name='J2', last_name='S2', date_of_birth='1995-01-01',
                                       phone_number='+112', location='Tashkent', education_level='bachelor')
        js3 = JobSeeker.objects.create(user=js3_user, first_name='J3', last_name='S3', date_of_birth='1996-01-01',
                                       phone_number='+113', location='Tashkent', education_level='bachelor')

        app1 = JobApplication.objects.create(
            job_posting=self.job_posting,
            job_seeker=self.job_seeker,
            cover_letter='CL1',
            status='applied',
            applied_date=timezone.now() - timedelta(days=2)
        )
        app2 = JobApplication.objects.create(
            job_posting=self.job_posting,
            job_seeker=js2,
            cover_letter='CL2',
            status='applied',
            applied_date=timezone.now() - timedelta(days=1)
        )
        app3 = JobApplication.objects.create(
            job_posting=self.job_posting,
            job_seeker=js3,
            cover_letter='CL3',
            status='applied',
            applied_date=timezone.now()
        )

        apps = list(JobApplication.objects.order_by('-applied_date'))
        self.assertEqual(apps[0].id, app3.id)
        self.assertEqual(apps[1].id, app2.id)
        self.assertEqual(apps[2].id, app1.id)

    def test_related_names(self):
        application = JobApplication.objects.create(**self.application_data)
        self.assertIn(application, self.job_posting.applications.all())
        self.assertIn(application, self.job_seeker.job_applications.all())
