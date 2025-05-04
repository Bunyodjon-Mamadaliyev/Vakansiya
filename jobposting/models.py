from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal

class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
    ]
    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level (0-2 years)'),
        ('mid', 'Mid Level (2-5 years)'),
        ('senior', 'Senior Level (5+ years)'),
        ('executive', 'Executive'),
    ]
    EDUCATION_REQUIRED_CHOICES = [
        ('none', 'No Formal Education'),
        ('high_school', 'High School Diploma'),
        ('vocational', 'Vocational Training'),
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('phd', 'PhD'),
    ]
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    location = models.CharField(max_length=150)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES,
                                        default='mid')
    education_required = models.CharField(max_length=20, choices=EDUCATION_REQUIRED_CHOICES,
                                          default='bachelor')
    salary_min = models.DecimalField(max_digits=10, decimal_places=2,
                                     validators=[MinValueValidator(Decimal('0.00'))])
    salary_max = models.DecimalField( max_digits=10, decimal_places=2,
                                      validators=[MinValueValidator(Decimal('0.00'))])
    skills_required = models.ManyToManyField('skill.Skill', related_name='job_postings', blank=True)
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateField()
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-posted_date']
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    @property
    def salary_range(self):
        return f"${self.salary_min:,.2f} - ${self.salary_max:,.2f}"

    @property
    def is_expired(self):
        return timezone.now().date() > self.deadline

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])