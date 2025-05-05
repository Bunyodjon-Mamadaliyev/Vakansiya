from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import JobSeeker
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import JobSeekerSerializer, ResumeUploadSerializer


class JobSeekerListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = JobSeekerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location', 'education_level', 'skills']

    def get_queryset(self):
        if self.request.user.is_staff:
            return JobSeeker.objects.all().select_related('user').prefetch_related('skills')
        return JobSeeker.objects.filter(user=self.request.user).select_related('user').prefetch_related('skills')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Ish qidiruvchilar ro'yxati muvaffaqiyatli olindi",
            "data": {
                "count": queryset.count(),
                "next": None,
                "previous": None,
                "results": serializer.data
            }
        })

    def create(self, request, *args, **kwargs):
        if hasattr(request.user, 'job_seeker'):
            return Response({
                "status": False,
                "message": "Sizda allaqachon profil mavjud"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "status": True,
            "message": "Ish qidiruvchi profili muvaffaqiyatli yaratildi",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JobSeekerRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": True,
            "message": "Ish qidiruvchi profili muvaffaqiyatli olindi",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": True,
            "message": "Ish qidiruvchi profili muvaffaqiyatli o'chirildi"
        }, status=status.HTTP_204_NO_CONTENT)

class ResumeUploadAPIView(generics.UpdateAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = ResumeUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({
            "status": True,
            "message": "Rezyume muvaffaqiyatli yuklandi",
            "data": {
                "id": instance.id,
                "resume": request.build_absolute_uri(instance.resume.url) if instance.resume else None
            }
        })