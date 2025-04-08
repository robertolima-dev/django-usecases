from django.contrib.auth.models import User
from django.db import models


class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, related_name="image") # noqa501
    original_image = models.ImageField(upload_to='uploads/original/') # noqa501
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/', null=True, blank=True) # noqa501
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_image.name
