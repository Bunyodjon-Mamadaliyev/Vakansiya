from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Employer
from .serializers import (
    EmployerSerializer,
    EmployerCreateSerializer,
    EmployerUpdateSerializer
)
from django.shortcuts import get_object_or_404


class IsEmployerUser(permissions.BasePermission):
    message = "Only employer users can access this endpoint."

    def has_permission(self, request, view):
        return request.user.user_type == 'employer'


class EmployerCreateAPIView(generics.CreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        employer = Employer.objects.get(id=serializer.data['id'])
        response_serializer = EmployerSerializer(employer)

        return Response(
            {
                "status": True,
                "message": "Employer profile created successfully",
                "data": response_serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class EmployerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Employer.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsEmployerUser]

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return EmployerUpdateSerializer
        return EmployerSerializer

    def get_object(self):
        return get_object_or_404(Employer, user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": True,
            "message": "Employer profile retrieved successfully",
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({
            "status": True,
            "message": "Employer profile updated successfully",
            "data": EmployerSerializer(instance).data
        })


class EmployerListAPIView(generics.ListAPIView):
    serializer_class = EmployerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'employer_profile') and \
                self.request.user.employer_profile.is_primary:
            return Employer.objects.filter(
                company=self.request.user.employer_profile.company
            )
        return Employer.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": True,
            "message": "Employers list retrieved successfully",
            "data": serializer.data
        })