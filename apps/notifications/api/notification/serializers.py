from rest_framework import serializers

from apps.notifications.models import Notification, UserNotificationRead


class NotificationSerializer(serializers.ModelSerializer):
    read = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'obj_code', 'obj_id', 'created_at', 'read']  # noqa: E501

    def get_read(self, obj):
        user = self.context['request'].user
        return UserNotificationRead.objects.filter(user=user, notification=obj).exists()  # noqa: E501
