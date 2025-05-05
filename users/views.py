from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import (
    CustomUserSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    LogoutSerializer
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': "Ro'yxatdan o'tishda xatolik yuz berdi",
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        data = CustomUserSerializer(user).data

        return Response({
            'status': True,
            'message': "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tkazildi",
            'data': data
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            response.data['status'] = True
            response.data['message'] = "Tizimga muvaffaqiyatli kirildi"
            response.data['data'] = {
                'access': response.data['access'],
                'refresh': response.data['refresh']
            }
            del response.data['access']
            del response.data['refresh']
        else:
            response.data = {
                'status': False,
                'message': "Tizimga kirishda xatolik yuz berdi",
                'errors': response.data
            }

        return response


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            response.data = {
                'status': True,
                'message': "Token muvaffaqiyatli yangilandi",
                'data': {
                    'access': response.data['access']
                }
            }
        else:
            response.data = {
                'status': False,
                'message': "Token yangilashda xatolik yuz berdi",
                'errors': response.data
            }
        return response

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': "Chiqishda xatolik yuz berdi",
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
            return Response({
                'status': True,
                'message': "Tizimdan muvaffaqiyatli chiqildi",
                'data': None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'message': str(e),
                'errors': None
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['profile'] = {}
        return Response({
            'status': True,
            'message': "Foydalanuvchi ma'lumotlari muvaffaqiyatli olindi",
            'data': data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': "Yangilashda xatolik yuz berdi",
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            'status': True,
            'message': "Foydalanuvchi ma'lumotlari muvaffaqiyatli yangilandi",
            'data': serializer.data
        })