# Generated by Django 5.0.3 on 2025-04-04 19:00

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("create", "Criação"),
                            ("update", "Atualização"),
                            ("delete", "Exclusão"),
                        ],
                        max_length=10,
                    ),
                ),
                ("model", models.CharField(max_length=100)),
                ("object_id", models.CharField(max_length=100)),
                ("object_repr", models.TextField()),
                ("changes", models.JSONField(blank=True, null=True)),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-timestamp"],
            },
        ),
    ]
