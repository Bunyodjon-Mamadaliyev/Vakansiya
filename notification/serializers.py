from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    is_recent = serializers.BooleanField(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'message', 'notification_type', 'related_object_id',
                  'is_read', 'created_at', 'is_recent']
        read_only_fields = ['created_at', 'is_recent']

class EmptySerializer(serializers.Serializer):
    pass