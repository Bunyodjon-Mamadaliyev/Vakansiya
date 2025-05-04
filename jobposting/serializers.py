from rest_framework import serializers
from .models import JobPosting
from skill.models import Skill
from company.serializers import CompanySerializer
from skill.serializers import SkillSerializer


class JobPostingSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    skills_required = SkillSerializer(many=True, read_only=True)
    salary_range = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = '__all__'
        read_only_fields = ('id', 'company', 'posted_date', 'views_count')

    def get_salary_range(self, obj):
        return f"${obj.salary_min:,.2f} - ${obj.salary_max:,.2f}"

    def get_is_expired(self, obj):
        return obj.is_expired

    def validate(self, data):
        if data.get('salary_min') and data.get('salary_max'):
            if data['salary_min'] > data['salary_max']:
                raise serializers.ValidationError({
                    'salary_min': "Minimal maosh maksimal maoshdan katta bo'lishi mumkin emas"
                })
        return data


class JobPostingCreateSerializer(serializers.ModelSerializer):
    skills_required = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all(),
        required=False
    )

    class Meta:
        model = JobPosting
        fields = '__all__'
        read_only_fields = ('id', 'company', 'posted_date', 'views_count')

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            if not request.user.is_authenticated:
                raise serializers.ValidationError({
                    'non_field_errors': ["Foydalanuvchi tizimga kirmagan."]
                })

            if not hasattr(request.user, 'company'):
                raise serializers.ValidationError({
                    'non_field_errors': ["Faqat kompaniyalar vakansiya e'lon qilishi mumkin."]
                })

        return data

    def create(self, validated_data):
        skills = validated_data.pop('skills_required', [])
        job_posting = JobPosting.objects.create(
            company=self.context['request'].user.company,
            **validated_data
        )
        job_posting.skills_required.set(skills)
        return job_posting


class RecommendedJobPostingSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    matching_skills = serializers.IntegerField()
    match_percentage = serializers.IntegerField()

    class Meta:
        model = JobPosting
        fields = (
            'id', 'company', 'title', 'location', 'job_type',
            'experience_level', 'salary_min', 'salary_max',
            'posted_date', 'deadline', 'matching_skills', 'match_percentage'
        )