from rest_framework import serializers

from apps.users.models import Profile


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    bio = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    phone = serializers.CharField(required=False)
    document = serializers.CharField(required=False)
    profession = serializers.CharField(required=False)
    avatar = serializers.URLField(required=False)
    confirm_email = serializers.BooleanField(required=False)
    unsubscribe = serializers.BooleanField(required=False)
    access_level = serializers.CharField(required=False)
    dt_updated = serializers.DateTimeField(required=False)
    dt_created = serializers.DateTimeField(required=False)


class ProfessionalSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    profile = serializers.SerializerMethodField(source='get_profile')

    def get_profile(self, value):
        profile = Profile.objects.filter(
            user_id=value.id
        ).first()
        if not profile:
            return {}
        profile_seralizer = ProfileSerializer(profile)
        return {
            'bio': profile_seralizer.data['bio'],
            'access_level': profile_seralizer.data['access_level'],
            'avatar': profile_seralizer.data['avatar'],
            'profession': profile_seralizer.data['profession'],
        }


class ProfessionalAllDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    profile = serializers.SerializerMethodField(source='get_profile')

    def get_profile(self, value):
        profile = Profile.objects.filter(
            user_id=value.id
        ).first()
        if not profile:
            return {}
        profile_seralizer = ProfileSerializer(profile)
        return {
            'bio': profile_seralizer.data['bio'],
            'access_level': profile_seralizer.data['access_level'],
            'avatar': profile_seralizer.data['avatar'],
            'profession': profile_seralizer.data['profession'],
        }
