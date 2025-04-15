from datetime import date

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.throttle.models import UserQuota
from apps.users.models import Profile

DEFAULT_ACTIONS = {
    "upload": 5,
    "report": 3,
    "api_access": 100,
}


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        for action, limit in DEFAULT_ACTIONS.items():
            quota, _ = UserQuota.objects.get_or_create(
                user=instance,
                action=action,
                defaults={
                    "limit": limit,
                    "used": 0,
                    "reset_date": date.today()
                }
            )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
