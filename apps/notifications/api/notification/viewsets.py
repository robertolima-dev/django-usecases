from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.notifications.api.notification.serializers import \
    NotificationSerializer
from apps.notifications.models import (Notification, UserNotificationDeleted,
                                       UserNotificationRead)


class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        deleted_ids = UserNotificationDeleted.objects.filter(user=user).values_list("notification_id", flat=True) # noqa501

        return Notification.objects.exclude(id__in=deleted_ids).order_by("-created_at") # noqa501

    @action(detail=True, methods=["patch"], url_path="mark-as-read")
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        UserNotificationRead.objects.get_or_create(user=request.user, notification=notification) # noqa501
        return Response({"detail": "Notificação marcada como lida."}, status=status.HTTP_200_OK) # noqa501

    def destroy(self, request, *args, **kwargs):
        notification = self.get_object()
        UserNotificationDeleted.objects.get_or_create(user=request.user, notification=notification) # noqa501
        return Response({"detail": "Notificação marcada como deletada."}, status=status.HTTP_204_NO_CONTENT) # noqa501
