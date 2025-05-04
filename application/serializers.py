from rest_framework import serializers
from .models import JobApplication
from jobposting.serializers import JobPostingSerializer
from jobseeker.serializers import JobSeekerSerializer

class JobApplicationSerializer(serializers.ModelSerializer):
    job_posting = JobPostingSerializer(read_only=True)
    job_seeker = JobSeekerSerializer(read_only=True)
    resume = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = [
            'id',
            'job_posting',
            'job_seeker',
            'cover_letter',
            'resume',
            'status',
            'applied_date',
            'updated_date'
        ]

    def get_resume(self, obj):
        request = self.context.get('request')
        if obj.resume and request:
            return request.build_absolute_uri(obj.resume.url)
        return None

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job_posting', 'cover_letter', 'resume']

    def validate(self, data):
        user = self.context['request'].user
        if not hasattr(user, 'jobseeker'):
            raise serializers.ValidationError("Only job seekers can submit applications")

        if not data.get('resume') and not user.jobseeker.resume:
            raise serializers.ValidationError("Resume is required or must exist in your profile")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        job_seeker = user.jobseeker

        if not validated_data.get('resume'):
            validated_data['resume'] = job_seeker.resume

        return JobApplication.objects.create(
            job_posting=validated_data['job_posting'],
            job_seeker=job_seeker,
            cover_letter=validated_data['cover_letter'],
            resume=validated_data['resume'],
        )

class JobApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['status']