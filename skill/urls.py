from django.urls import path
from .views import SkillListCreateAPIView

urlpatterns = [
    path('skills/', SkillListCreateAPIView.as_view(), name='skill-list-create'),
]