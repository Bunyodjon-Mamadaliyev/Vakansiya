from django.urls import path
from .views import (
    JobPostingListCreateView,
    JobPostingRetrieveUpdateDestroyView,
    RecommendedJobPostingListView
)

urlpatterns = [
    path('job-postings/', JobPostingListCreateView.as_view(), name='job-posting-list-create'),
    path('job-postings/<int:id>/', JobPostingRetrieveUpdateDestroyView.as_view(), name='job-posting-detail'),
    path('job-postings/recommended/', RecommendedJobPostingListView.as_view(), name='recommended-job-postings'),
]