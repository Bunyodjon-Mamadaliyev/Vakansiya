from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from .models import JobApplication
from django.http import Http404
from .serializers import (
    JobApplicationSerializer,
    JobApplicationCreateSerializer,
    JobApplicationStatusSerializer
)
from jobposting.models import JobPosting
from django.shortcuts import get_object_or_404


class JobApplicationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = JobApplication.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobApplicationCreateSerializer
        return JobApplicationSerializer

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'job_seeker'):
            raise serializers.ValidationError("Only job seekers can submit applications")
        serializer.save(job_seeker=self.request.user.job_seeker)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            instance = serializer.instance  # Get the created instance directly from serializer

            full_serializer = JobApplicationSerializer(instance, context={'request': request})

            return Response({
                'status': True,
                'message': 'Ariza muvaffaqiyatli topshirildi',
                'data': full_serializer.data
            }, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            return Response({
                'status': False,
                'message': str(e),
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Xatolik yuz berdi',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if hasattr(user, 'job_seeker'):
            return queryset.filter(job_seeker=user.job_seeker)
        elif hasattr(user, 'employer_profile'):
            return queryset.filter(job_posting__company=user.employer_profile.company)
        return queryset.none()


class JobApplicationRetrieveView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobApplicationSerializer
    queryset = JobApplication.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class JobApplicationStatusUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobApplicationStatusSerializer
    queryset = JobApplication.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        full_serializer = JobApplicationSerializer(instance, context={'request': request})
        return Response({
            'status': True,
            'message': 'Status muvaffaqiyatli yangilandi',
            'data': full_serializer.data
        })


class JobPostingApplicationsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'company'):
            raise Http404("Sizning profilingizga biron bir kompaniya biriktirilmagan.")

        job_posting = get_object_or_404(
            JobPosting.objects.filter(company=user.company),
            pk=self.kwargs['pk']
        )
        return JobApplication.objects.filter(job_posting=job_posting)