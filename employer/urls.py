from django.urls import path
from .views import (
    EmployerCreateAPIView,
    EmployerRetrieveUpdateAPIView,
    EmployerListAPIView
)

urlpatterns = [
    path('employers/', EmployerListAPIView.as_view(), name='employer-list'),
    path('employers/create/', EmployerCreateAPIView.as_view(), name='employer-create'),
    path('employers/me/', EmployerRetrieveUpdateAPIView.as_view(), name='employer-detail'),
]