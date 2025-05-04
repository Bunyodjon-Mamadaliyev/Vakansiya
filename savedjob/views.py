# views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import SavedJob
from .serializers import SavedJobSerializer, SaveJobSerializer
from django.shortcuts import get_object_or_404


class SavedJobListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SaveJobSerializer
        return SavedJobSerializer

    def get_queryset(self):
        return SavedJob.objects.filter(
            job_seeker=self.request.user.jobseeker
        ).select_related(
            'job_posting',
            'job_posting__company'
        ).order_by('-saved_date')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Saqlangan vakansiyalar ro'yxati muvaffaqiyatli olindi",
            "data": {
                "count": queryset.count(),
                "next": None,
                "previous": None,
                "results": serializer.data
            }
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved_job = serializer.save()

        # Return the full saved job details
        response_serializer = SavedJobSerializer(saved_job, context={'request': request})
        return Response({
            "status": True,
            "message": "Vakansiya muvaffaqiyatli saqlandi",
            "data": response_serializer.data
        }, status=status.HTTP_201_CREATED)


class SavedJobRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SavedJobSerializer

    def get_queryset(self):
        return SavedJob.objects.filter(job_seeker=self.request.user.jobseeker)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": True,
            "message": "Saqlangan vakansiya muvaffaqiyatli olindi",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status": True,
            "message": "Vakansiya saqlanganlar ro'yxatidan muvaffaqiyatli o'chirildi"
        }, status=status.HTTP_204_NO_CONTENT)