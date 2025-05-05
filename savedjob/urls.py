from django.urls import path
from .views import SavedJobListCreateAPIView, SavedJobRetrieveDestroyAPIView

urlpatterns = [
    path('saved-jobs/', SavedJobListCreateAPIView.as_view(), name='saved-jobs-list'),
    path('saved-jobs/<int:pk>/', SavedJobRetrieveDestroyAPIView.as_view(), name='saved-job-detail'),
]