from django.contrib.auth.models import User
from django.db import models


class UploadedImage(models.Model):
    FORMAT_CHOICES = [
        ('JPEG', 'JPEG'),
        ('WEBP', 'WebP'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, related_name="image") # noqa501
    original_image = models.ImageField(upload_to='uploads/original/')
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/', null=True, blank=True) # noqa501
    medium = models.ImageField(upload_to='uploads/medium/', null=True, blank=True) # noqa501
    large = models.ImageField(upload_to='uploads/large/', null=True, blank=True) # noqa501
    output_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='JPEG') # noqa501
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_image.name
