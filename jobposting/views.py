from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from .models import JobPosting
from django.db.models import Count, Q, F, ExpressionWrapper, FloatField
from django.db.models.functions import Greatest
from .serializers import (
    JobPostingSerializer,
    JobPostingCreateSerializer,
    RecommendedJobPostingSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone


class JobPostingListCreateView(generics.ListCreateAPIView):
    queryset = JobPosting.objects.filter(is_active=True, deadline__gte=timezone.now().date())
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'job_type', 'experience_level', 'education_required']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['posted_date', 'salary_min', 'salary_max']
    ordering = ['-posted_date']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobPostingCreateSerializer
        return JobPostingSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': "Vakansiya yaratishda xatolik yuz berdi",
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        job_posting = serializer.save()

        return Response({
            'status': True,
            'message': "Vakansiya muvaffaqiyatli e'lon qilindi",
            'data': JobPostingSerializer(job_posting, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response({
            'status': True,
            'message': "Vakansiyalar muvaffaqiyatli olindi",
            'data': serializer.data
        })


class JobPostingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)

        return Response({
            'status': True,
            'message': "Vakansiya ma'lumotlari muvaffaqiyatli olindi",
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.company.user != request.user:
            return Response({
                'status': False,
                'message': "Faqat vakansiya egasi uni tahrirlashi mumkin",
                'errors': {
                    'non_field_errors': ["Siz bu vakansiyani tahrirlash huquqiga ega emassiz."]
                }
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': "Vakansiyani yangilashda xatolik yuz berdi",
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            'status': True,
            'message': "Vakansiya muvaffaqiyatli yangilandi",
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.company.user != request.user:
            return Response({
                'status': False,
                'message': "Faqat vakansiya egasi uni o'chirishi mumkin",
                'errors': {
                    'non_field_errors': ["Siz bu vakansiyani o'chirish huquqiga ega emassiz."]
                }
            }, status=status.HTTP_403_FORBIDDEN)

        instance.delete()

        return Response({
            'status': True,
            'message': "Vakansiya muvaffaqiyatli o'chirildi",
            'data': None
        }, status=status.HTTP_204_NO_CONTENT)


class RecommendedJobPostingListView(generics.ListAPIView):
    serializer_class = RecommendedJobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Check if the user has a profile before accessing skills
        try:
            user_skills = self.request.user.profile.skills.all()
        except AttributeError:  # Handle case where profile does not exist
            user_skills = []

        # Filter job postings based on user skills
        queryset = JobPosting.objects.filter(
            is_active=True,
            deadline__gte=timezone.now().date(),
            skills_required__in=user_skills
        )

        # Annotate the matching skills and total skills
        queryset = queryset.annotate(
            matching_skills=Count('skills_required', filter=Q(skills_required__in=user_skills)),
            total_skills=Greatest(Count('skills_required'), 1)
        )

        # Calculate the match percentage
        queryset = queryset.annotate(
            match_percentage=ExpressionWrapper(
                F('matching_skills') * 100.0 / F('total_skills'),
                output_field=FloatField()
            )
        )

        # Remove duplicates and order by match percentage and posted date
        queryset = queryset.distinct().order_by('-match_percentage', '-posted_date')[:10]

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'status': True,
            'message': "Tavsiya etilgan vakansiyalar muvaffaqiyatli olindi",
            'data': {
                'count': len(serializer.data),
                'next': None,
                'previous': None,
                'results': serializer.data
            }
        })