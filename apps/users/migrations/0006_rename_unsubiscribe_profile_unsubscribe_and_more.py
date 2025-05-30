# Generated by Django 5.0.3 on 2024-03-08 12:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_hash_unique_user_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="unsubiscribe",
            new_name="unsubscribe",
        ),
        migrations.AlterField(
            model_name="hash",
            name="type",
            field=models.CharField(
                choices=[
                    ("confirm_email", "confirm_email"),
                    ("change_password", "change_password"),
                    ("unsubscribe", "unsubscribe"),
                ],
                default="confirm_email",
                max_length=25,
            ),
        ),
    ]
