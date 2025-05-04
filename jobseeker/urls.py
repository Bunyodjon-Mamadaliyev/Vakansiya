# urls.py
from django.urls import path
from .views import (
    JobSeekerListCreateAPIView,
    JobSeekerRetrieveDestroyAPIView,
    ResumeUploadAPIView
)

urlpatterns = [
    path('job-seekers/', JobSeekerListCreateAPIView.as_view(), name='job-seeker-create'),
    path('job-seekers/<int:pk>/', JobSeekerRetrieveDestroyAPIView.as_view(), name='job-seeker-detail'),
    path('job-seekers/<int:pk>/upload-resume/', ResumeUploadAPIView.as_view(), name='job-seeker-upload-resume'),
]
