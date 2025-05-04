from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
from django.shortcuts import get_object_or_404


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Company.objects.all()

    def perform_create(self, serializer):
        if Company.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError("Siz allaqachon kompaniya yaratgansiz.")
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': True,
            'message': "Kompaniyalar ro'yxati muvaffaqiyatli olindi",
            'data': {
                'count': response.data['count'],
                'next': response.data['next'],
                'previous': response.data['previous'],
                'results': response.data['results']
            }
        })

    def create(self, request, *args, **kwargs):
        if Company.objects.filter(user=request.user).exists():
            return Response({
                "status": False,
                "message": "Siz allaqachon kompaniya yaratgansiz."
            }, status=400)

        return super().create(request, *args, **kwargs)


class CompanyRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})

        response_data = {
            "status": True,
            "message": "Kompaniya ma'lumotlari muvaffaqiyatli olindi",
            "data": serializer.data
        }
        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        response_data = {
            "status": True,
            "message": "Kompaniya muvaffaqiyatli o'chirildi",
            "data": None
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)