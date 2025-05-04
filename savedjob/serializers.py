# serializers.py
from rest_framework import serializers
from .models import SavedJob
from jobposting.serializers import JobPostingSerializer  # Assuming you have this


class SavedJobSerializer(serializers.ModelSerializer):
    job_posting = serializers.SerializerMethodField()
    is_job_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = SavedJob
        fields = ['id', 'job_posting', 'saved_date', 'is_job_active']
        read_only_fields = ['saved_date', 'is_job_active']

    def get_job_posting(self, obj):
        from jobposting.serializers import JobPostingSerializer  # Avoid circular import
        return JobPostingSerializer(obj.job_posting, context=self.context).data


class SaveJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = ['job_posting']

    def validate_job_posting(self, value):
        # Check if job posting exists and is active
        if not value.is_active:
            raise serializers.ValidationError("This job posting is no longer active")
        if value.is_expired:
            raise serializers.ValidationError("This job posting has expired")
        return value

    def create(self, validated_data):
        job_seeker = self.context['request'].user.jobseeker
        job_posting = validated_data['job_posting']

        # Check if already saved
        if SavedJob.objects.filter(job_seeker=job_seeker, job_posting=job_posting).exists():
            raise serializers.ValidationError({"detail": "Job already saved"})

        return SavedJob.objects.create(job_seeker=job_seeker, **validated_data)