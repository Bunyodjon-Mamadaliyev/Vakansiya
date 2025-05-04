from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from jobposting.models import JobPosting
from company.models import Company
from skill.models import Skill


class JobPostingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample company
        cls.company = Company.objects.create(name="TechCorp", location="New York")

        # Create a sample skill
        cls.skill1 = Skill.objects.create(name="Python", category="technical")
        cls.skill2 = Skill.objects.create(name="JavaScript", category="technical")

        # Create a job posting instance
        cls.job_posting = JobPosting.objects.create(
            company=cls.company,
            title="Software Developer",
            description="Develop software applications.",
            requirements="Experience with Python and Django.",
            responsibilities="Build and maintain web applications.",
            location="New York",
            job_type="full_time",
            experience_level="mid",
            education_required="bachelor",
            salary_min=Decimal('50000.00'),
            salary_max=Decimal('90000.00'),
            deadline="2025-12-31",
        )

        # Add skills to the job posting
        cls.job_posting.skills_required.add(cls.skill1, cls.skill2)

    def test_job_posting_str(self):
        # Test the __str__ method
        self.assertEqual(str(self.job_posting), "Software Developer at TechCorp")

    def test_job_posting_salary_range(self):
        # Test the salary_range property
        self.assertEqual(self.job_posting.salary_range, "$50,000.00 - $90,000.00")

    def test_job_posting_is_expired(self):
        # Test the is_expired property
        self.assertFalse(self.job_posting.is_expired)  # As the deadline is in the future

        # Set an expired deadline for the test
        self.job_posting.deadline = "2020-12-31"
        self.job_posting.save()
        self.assertTrue(self.job_posting.is_expired)  # As the deadline is in the past

    def test_job_posting_increment_views(self):
        # Test incrementing the views_count field
        initial_views = self.job_posting.views_count
        self.job_posting.increment_views()
        self.assertEqual(self.job_posting.views_count, initial_views + 1)

    def test_job_posting_ordering(self):
        # Create another job posting with a later posted date
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
        )

        # Verify that job postings are ordered by posted_date (latest first)
        job_postings = JobPosting.objects.all()
        self.assertEqual(job_postings[0], self.job_posting)
        self.assertEqual(job_postings[1], later_posted_job)

    def test_job_posting_default_active_status(self):
        # Test the default value of the 'is_active' field
        self.assertTrue(self.job_posting.is_active)

    def test_job_posting_skills_required(self):
        # Test that the job posting has the correct skills
        self.assertIn(self.skill1, self.job_posting.skills_required.all())
        self.assertIn(self.skill2, self.job_posting.skills_required.all())
