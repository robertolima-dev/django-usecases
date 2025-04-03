from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.api.profile.serializers import ProfileSerializer
from apps.users.models import Profile

UserModel = get_user_model()


class UserSigninSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


class UserSerializer(UserSimpleSerializer):
    profile = serializers.SerializerMethodField(source='get_profile')

    def get_profile(self, value):
        profile = Profile.objects.filter(
            user_id=value.id
        ).first()
        if not profile:
            return {}
        profile_seralizer = ProfileSerializer(profile)
        return profile_seralizer.data


class CreateUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    community = serializers.IntegerField(required=False, allow_null=True)


class ConfirmEmailSerializer(serializers.Serializer):
    hash = serializers.CharField(required=True)


class UnsubscribeSerializer(serializers.Serializer):
    hash = serializers.CharField(required=True)
    unsubscribe = serializers.BooleanField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    hash = serializers.CharField(required=False)
    jwt = serializers.CharField(required=False)


class ForgorPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
