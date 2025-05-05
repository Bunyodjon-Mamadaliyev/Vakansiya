from django.test import TestCase
from django.contrib.auth import get_user_model
from company.models import Company
from employer.models import Employer

User = get_user_model()

class EmployerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='employer1',
            password='pass123',
            user_type='employer',
            first_name='Ali',
            last_name='Valiyev'
        )
        self.company = Company.objects.create(
            user=self.user,
            name='Techno Group',
            description='A tech company',
            industry='it',
            location='Tashkent',
            employees_count=20
        )

    def test_create_employer_successfully(self):
        employer = Employer.objects.create(
            user=self.user,
            company=self.company,
            position='HR Manager'
        )
        self.assertEqual(employer.user, self.user)
        self.assertEqual(employer.company, self.company)
        self.assertEqual(employer.position, 'HR Manager')
        self.assertFalse(employer.is_primary)

    def test_str_method(self):
        employer = Employer.objects.create(
            user=self.user,
            company=self.company,
            position='Team Lead'
        )
        self.assertEqual(str(employer), "Ali Valiyev (Team Lead)")

    def test_company_nullable(self):
        employer = Employer.objects.create(
            user=self.user,
            position='Recruiter'
        )
        self.assertIsNone(employer.company)
