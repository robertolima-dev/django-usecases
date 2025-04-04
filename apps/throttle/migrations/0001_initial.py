# Generated by Django 5.0.3 on 2025-04-05 12:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserQuota",
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
                            ("api_access", "API Access"),
                            ("upload", "Upload de Arquivo"),
                            ("report", "Geração de Relatório"),
                        ],
                        max_length=50,
                    ),
                ),
                ("limit", models.PositiveIntegerField(default=100)),
                ("used", models.PositiveIntegerField(default=0)),
                ("reset_date", models.DateField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quotas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "action")},
            },
        ),
    ]
