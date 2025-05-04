from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    # O'qish uchun (GET so'rovlarida) industry display qiymatini qaytarish
    industry_display = serializers.CharField(source='get_industry_display', read_only=True)

    # Logo uchun to'liq URL
    logo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'industry',
            'industry_display',  # Faqat o'qish uchun
            'location',
            'logo',  # Yuklash uchun
            'logo_url',  # Faqat o'qish uchun
            'employees_count'
        ]
        extra_kwargs = {
            'industry': {'write_only': True},  # POST/PATCH uchun
            'logo': {'write_only': True},  # POST/PATCH uchun
        }

    def get_logo_url(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(obj.logo.url)
        return None