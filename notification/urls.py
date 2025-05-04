from django.urls import path
from .views import (
    NotificationListCreateAPIView,
    NotificationDetailAPIView,
    MarkNotificationAsReadAPIView,
    MarkAllNotificationsAsReadAPIView
)

urlpatterns = [
    path('notifications/', NotificationListCreateAPIView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationDetailAPIView.as_view(), name='notification-detail'),
    path('notifications/<int:pk>/read/', MarkNotificationAsReadAPIView.as_view(), name='mark-notification-read'),
    path('notifications/read-all/', MarkAllNotificationsAsReadAPIView.as_view(), name='mark-all-notifications-read'),
]