from django.db import models
from django.utils import timezone

# Create your models here.


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModelAllManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True, db_index=True, null=True, ) # noqa501
    created_at = models.DateTimeField(auto_now_add=True, null=True, ) # noqa501
    deleted_at = models.DateTimeField(null=True, blank=True) # noqa501

    objects = BaseModelManager()
    obj_all = BaseModelAllManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def force_delete(self):
        super(BaseModel, self).delete()
