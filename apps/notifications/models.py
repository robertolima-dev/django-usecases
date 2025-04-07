from django.contrib.auth import get_user_model
from django.db import models

from api_core.models import BaseModel

User = get_user_model()


class Notification(BaseModel):
    title = models.CharField(max_length=120, null=True, blank=True, )
    message = models.TextField()
    obj_code = models.CharField(max_length=50, default="platform", db_index=True)  # noqa501
    obj_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserNotificationRead(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_index=True) # noqa501
    notification = models.ForeignKey(Notification, on_delete=models.SET_NULL, null=True, db_index=True) # noqa501


class UserNotificationDeleted(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_index=True) # noqa501
    notification = models.ForeignKey(Notification, on_delete=models.SET_NULL, null=True, db_index=True) # noqa501
