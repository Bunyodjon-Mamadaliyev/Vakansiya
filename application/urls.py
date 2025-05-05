from django.urls import path
from . import views

urlpatterns = [
    path('applications/', views.JobApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', views.JobApplicationRetrieveView.as_view(), name='application-detail'),
    path('applications/<int:pk>/status/', views.JobApplicationStatusUpdateView.as_view(),name='application-status-update'),
    path('job-postings/<int:pk>/applications/', views.JobPostingApplicationsListView.as_view(),name='jobposting-applications'),
]