from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.backends.s3boto3 import S3Boto3Storage


class AWSMediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


class GCPMediaStorage(GoogleCloudStorage):
    location = "media"
    file_overwrite = False


def get_storage():
    if getattr(settings, "FILE_PROVIDER", 'aws'):
        return AWSMediaStorage()
    return GCPMediaStorage()
