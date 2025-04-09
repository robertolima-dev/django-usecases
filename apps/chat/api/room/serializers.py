from rest_framework import serializers

from apps.chat.models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'user1', 'user2', 'created_at']
        read_only_fields = ['id', 'created_at']
