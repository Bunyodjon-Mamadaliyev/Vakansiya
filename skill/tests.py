from django.test import TestCase
from django.core.exceptions import ValidationError
from skill.models import Skill

class SkillModelTest(TestCase):

    def test_create_skill_successfully(self):
        skill = Skill.objects.create(name="Python", category="technical")
        self.assertEqual(skill.name, "Python")
        self.assertEqual(skill.category, "technical")

    def test_create_skill_invalid_category(self):
        skill = Skill(name="Invalid Skill", category="invalid_category")
        with self.assertRaises(ValidationError):
            skill.clean()  # This should raise ValidationError

    def test_create_duplicate_skill_name(self):
        Skill.objects.create(name="Python", category="technical")
        with self.assertRaises(Exception):  # Unique constraint violation
            Skill.objects.create(name="Python", category="technical")

    def test_skill_ordering(self):
        skill1 = Skill.objects.create(name="Python", category="technical")
        skill2 = Skill.objects.create(name="Java", category="technical")
        skills = Skill.objects.all()
        self.assertEqual(list(skills), [skill2, skill1])  # Skills should be ordered alphabetically
