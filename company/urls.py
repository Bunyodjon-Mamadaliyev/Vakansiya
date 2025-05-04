from django.urls import path
from .views import CompanyListCreateView, CompanyRetrieveDestroyView

urlpatterns = [
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:id>/', CompanyRetrieveDestroyView.as_view(), name='company-retrieve-destroy'),
]