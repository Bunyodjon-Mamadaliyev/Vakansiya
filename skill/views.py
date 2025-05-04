from rest_framework.response import Response
from rest_framework import generics, status
from .models import Skill
from .serializers import SkillSerializer
from rest_framework.permissions import IsAuthenticated

class SkillListCreateAPIView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "status": True,
            "message": "Ko'nikmalar ro'yxati",
            "data": response.data
        })

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": True,
            "message": "Ko'nikma muvaffaqiyatli qo'shildi",
            "data": response.data
        }, status=status.HTTP_201_CREATED)