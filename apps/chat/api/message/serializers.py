from rest_framework import serializers

from apps.chat.models import Message, Room


class MessageCreateSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ['room_id', 'content']

    def validate_room_id(self, value):
        request_user = self.context['request'].user
        try:
            room = Room.objects.get(id=value)
            if request_user != room.user1 and request_user != room.user2: # noqa501
                raise serializers.ValidationError("Você não tem permissão para enviar mensagens nesta sala.") # noqa501
            return value
        except Room.DoesNotExist:
            raise serializers.ValidationError("Sala não encontrada.") # noqa501

    def create(self, validated_data):
        room = Room.objects.get(id=validated_data['room_id']) # noqa501
        return Message.objects.create(
            room=room,
            sender=self.context['request'].user,
            content=validated_data['content']
        )


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True) # noqa501

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'sender_username', 'content', 'timestamp', 'is_read'] # noqa501
