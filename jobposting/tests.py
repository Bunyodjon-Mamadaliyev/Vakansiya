from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from jobposting.models import JobPosting, JobCategory
from company.models import Company
from skill.models import Skill
from django.contrib.auth import get_user_model

User = get_user_model()

class JobPostingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345', user_type='employer')
        cls.company = Company.objects.create(
            user=cls.user,
            name="TechCorp",
            description="A tech company",
            website="https://techcorp.com",
            industry="it",
            location="New York"
        )
        cls.category = JobCategory.objects.create(name="IT")
        cls.skill1 = Skill.objects.create(name="Python")
        cls.skill2 = Skill.objects.create(name="Django")
        cls.job_posting = JobPosting.objects.create(
            company=cls.company,
            title="Backend Developer",
            description="Develop backend systems",
            requirements="Experience with Django",
            responsibilities="Build APIs",
            location="Remote",
            salary_min=Decimal('5000.00'),
            salary_max=Decimal('8000.00'),
            deadline=timezone.now().date() + timezone.timedelta(days=30),
            posted_date=timezone.now()
        )
        cls.job_posting.skills_required.add(cls.skill1, cls.skill2)

    def test_job_posting_str(self):
        self.assertEqual(str(self.job_posting), "Backend Developer at TechCorp")

    def test_job_posting_salary_range(self):
        self.assertEqual(self.job_posting.salary_range, "$5,000.00 - $8,000.00")

    def test_job_posting_is_expired(self):
        self.assertFalse(self.job_posting.is_expired)
        self.job_posting.deadline = timezone.datetime(2020, 12, 31).date()
        self.job_posting.save()
        self.assertTrue(self.job_posting.is_expired)

    def test_job_posting_increment_views(self):
        initial_views = self.job_posting.views_count
        self.job_posting.increment_views()
        self.assertEqual(self.job_posting.views_count, initial_views + 1)

    def test_job_posting_ordering(self):
        later_posted_job = JobPosting.objects.create(
            company=self.company,
            title="Data Scientist",
            description="Analyze and interpret complex data.",
            requirements="Experience with data analysis.",
            responsibilities="Data modeling and reporting.",
            location="New York",
            job_type="full_time",
            experience_level="entry",
            education_required="bachelor",
            salary_min=Decimal('60000.00'),
            salary_max=Decimal('95000.00'),
            deadline="2025-12-31",
            posted_date=timezone.now() + timezone.timedelta(days=1)
        )
        job_postings = JobPosting.objects.all()
        self.assertEqual(job_postings[0], later_posted_job)
        self.assertEqual(job_postings[1], self.job_posting)

    def test_job_posting_default_active_status(self):
        self.assertTrue(self.job_posting.is_active)

    def test_job_posting_skills_required(self):
        self.assertIn(self.skill1, self.job_posting.skills_required.all())
        self.assertIn(self.skill2, self.job_posting.skills_required.all())
