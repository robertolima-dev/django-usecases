import binascii
import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

ACCESS_LEVEL_CHOICES = (
    ('user', 'user'),
    ('professional_free', 'professional_free'),
    ('professional_basic', 'professional_basic'),
    ('professional_premium', 'professional_premium'),
    ('admin', 'admin'),
    ('super_admin', 'super_admin'),
)

HASH_TYPE_CHOICES = (
    ('confirm_email', 'confirm_email'),
    ('change_password', 'change_password'),
    ('unsubscribe', 'unsubscribe'),
)


def get_user_format_name(self):
    return f"{self.email} / {self.first_name}"


User.add_to_class("__str__", get_user_format_name)


class BaseModel(models.Model):
    dt_updated = models.DateTimeField(auto_now=True, db_index=True, null=True, ) # noqa501
    dt_created = models.DateTimeField(auto_now_add=True, null=True, ) # noqa501

    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    document = models.CharField(max_length=30, blank=True, null=True)
    profession = models.CharField(max_length=120, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    confirm_email = models.BooleanField(default=False)
    unsubscribe = models.BooleanField(default=False)
    access_level = models.CharField(
        max_length=25,
        choices=ACCESS_LEVEL_CHOICES,
        default='user',
        db_index=True,
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self) -> str:
        return str(self.user.email)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Hash(models.Model):
    hash = models.CharField(_("Key"), max_length=40, primary_key=True, db_index=True) # noqa501
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    type = models.CharField(
        max_length=25,
        choices=HASH_TYPE_CHOICES,
        default='confirm_email',
        db_index=True
    )

    class Meta:
        verbose_name = _("Hash")
        verbose_name_plural = _("Hashes")
        constraints = [
            UniqueConstraint(
                fields=[
                    'user',
                    'type',
                ],
                name='unique_user_type'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = self.generate_hash()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_hash(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.hash


class AddressUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    street = models.CharField(max_length=255, null=True, blank=True,)
    number = models.CharField(max_length=10, null=True, blank=True,)
    zipcode = models.CharField(max_length=20, null=True, blank=True,)
    neighborhood = models.CharField(max_length=120, null=True, blank=True,)
    city = models.CharField(max_length=120, null=True, blank=True,)
    state = models.CharField(max_length=120, null=True, blank=True,)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return f"Endereço do user: {self.user.email}"
