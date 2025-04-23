from rest_framework import serializers


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
