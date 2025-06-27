from django.contrib.auth import get_user_model
from django.db import models

from api_core.models import BaseModel

User = get_user_model()


class Tenant(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True, blank=True, null=True)  # noqa: E501
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tenants')  # noqa: E501
    users = models.ManyToManyField(User, related_name='tenants')  # noqa: E501

    def __str__(self):
        return self.name


class Project(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='projects')  # noqa: E501
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"
