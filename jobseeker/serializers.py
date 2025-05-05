from rest_framework import serializers
from .models import JobSeeker
from skill.models import Skill
from django.contrib.auth import get_user_model
from skill.serializers import SkillSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email']

class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        source='skills',
        many=True,
        write_only=True,
        required=False
    )
    age = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = JobSeeker
        fields = [
            'id', 'user', 'first_name', 'last_name', 'date_of_birth',
            'phone_number', 'location', 'bio', 'skills', 'skill_ids',
            'experience_years', 'education_level', 'resume',
            'profile_picture', 'age', 'full_name'
        ]
        read_only_fields = ['user', 'resume', 'profile_picture']

    def validate_education_level(self, value):
        value = value.lower()
        choices = [choice[0] for choice in JobSeeker.EDUCATION_LEVEL_CHOICES]
        if value not in choices:
            raise serializers.ValidationError("Noto'g'ri ta'lim darajasi")
        return value

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ['resume']
        extra_kwargs = {
            'resume': {'required': True}
        }

    def update(self, instance, validated_data):
        if instance.resume:
            instance.resume.delete()
        return super().update(instance, validated_data)