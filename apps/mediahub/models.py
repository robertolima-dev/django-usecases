import hashlib
import os
from datetime import datetime

from django.db import models


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    name = os.path.splitext(filename)[0]
    timestamp = datetime.now().isoformat()
    hash_name = hashlib.sha256(f"{name}{timestamp}".encode()).hexdigest()
    return f"mediahub/{hash_name}.{ext}"


class MediaFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
