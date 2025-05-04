from django.urls import path
from . import views

urlpatterns = [
    # GET all applications (filtered by user type), POST new application
    path('applications/', views.JobApplicationListCreateView.as_view(), name='application-list-create'),

    # GET single application details
    path('applications/<int:pk>/', views.JobApplicationRetrieveView.as_view(), name='application-detail'),

    # UPDATE application status
    path('applications/<int:pk>/status/', views.JobApplicationStatusUpdateView.as_view(),
         name='application-status-update'),

    # GET all applications for a specific job posting
    path('job-postings/<int:pk>/applications/', views.JobPostingApplicationsListView.as_view(),
         name='jobposting-applications'),
]