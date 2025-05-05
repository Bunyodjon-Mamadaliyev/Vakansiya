from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    industry_display = serializers.CharField(source='get_industry_display', read_only=True)
    logo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'industry', 'industry_display', 'location',
                  'logo', 'logo_url', 'employees_count']
        extra_kwargs = {
            'industry': {'write_only': True},
            'logo': {'write_only': True},
        }

    def get_logo_url(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(obj.logo.url)
        return None