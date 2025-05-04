# employer/serializers.py
from rest_framework import serializers
from .models import Employer
from company.serializers import CompanySerializer  # Assuming you have this


class EmployerSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employer
        fields = [
            'id', 'user', 'email', 'full_name', 'company',
            'position', 'is_primary'
        ]
        read_only_fields = ['user', 'company', 'is_primary']

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class EmployerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['position']

    def create(self, validated_data):
        user = self.context['request'].user
        if hasattr(user, 'employer_profile'):
            raise serializers.ValidationError("User already has an employer profile")

        return Employer.objects.create(
            user=user,
            **validated_data
        )


class EmployerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['position', 'is_primary']

    def validate_is_primary(self, value):
        if value and not self.instance.company:
            raise serializers.ValidationError(
                "Cannot set as primary without a company"
            )
        return value