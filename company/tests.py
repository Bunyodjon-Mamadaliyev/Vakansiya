from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from company.models import Company
from django.db.models.fields.files import ImageFieldFile

User = get_user_model()

class CompanyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='employer1', password='pass123', user_type='employer')

    def test_create_company_successfully(self):
        company = Company.objects.create(
            user=self.user,
            name='Test Corp',
            description='A test company',
            website='https://testcorp.com',
            industry='it',
            location='Tashkent',
            founded_year=2000,
            employees_count=10
        )
        self.assertEqual(company.name, 'Test Corp')
        self.assertEqual(company.description, 'A test company')
        self.assertEqual(company.website, 'https://testcorp.com')
        self.assertEqual(company.industry, 'it')
        self.assertEqual(company.location, 'Tashkent')
        self.assertEqual(company.founded_year, 2000)
        self.assertEqual(company.employees_count, 10)
        self.assertEqual(str(company), 'Test Corp')

    def test_founded_year_validation(self):
        company = Company(
            user=self.user,
            name='Old Corp',
            description='Old description',
            industry='finance',
            location='Bukhara',
            founded_year=1700,
            employees_count=5
        )
        with self.assertRaises(ValidationError):
            company.full_clean()

    def test_employees_count_must_be_positive(self):
        company = Company(
            user=self.user,
            name='Zero Employees Corp',
            description='Still testing',
            industry='retail',
            location='Samarkand',
            employees_count=0
        )
        with self.assertRaises(ValidationError):
            company.full_clean()

    def test_optional_fields_blank(self):
        company = Company.objects.create(
            user=self.user,
            name='No Website Corp',
            description='No website provided',
            industry='other',
            location='Andijan',
            employees_count=3
        )
        self.assertEqual(company.website, '')
        self.assertIsInstance(company.logo,ImageFieldFile)
        self.assertIsNone(company.logo.name)
