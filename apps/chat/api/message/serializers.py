from rest_framework import serializers

from apps.chat.models import Message, Room


class MessageCreateSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ['room_id', 'type_message', 'content']

    def validate_room_id(self, value):
        user = self.context['request'].user
        try:
            room = Room.objects.get(id=value)
        except Room.DoesNotExist:
            raise serializers.ValidationError("Sala não encontrada.")

        if not room.users.filter(id=user.id).exists():
            raise serializers.ValidationError("Você não faz parte desta sala.") # noqa501
        return value

    def create(self, validated_data):
        room = Room.objects.get(id=validated_data['room_id'])
        sender = self.context['request'].user
        return Message.objects.create(
            room=room,
            sender=sender,
            type_message=validated_data.get('type_message', 'text'),
            content=validated_data['content']
        )


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True) # noqa501
    sender_avatar = serializers.CharField(source='sender.profile.avatar', read_only=True) # noqa501

    class Meta:
        model = Message
        fields = [
            'id',
            'room',
            'sender_id',
            'sender_username',
            'sender_avatar',
            'type_message',
            'content',
            'timestamp',
            'is_read',
        ]
