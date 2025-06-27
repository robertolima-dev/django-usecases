from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.chat.models import Message, Room

User = get_user_model()


class RoomCreateSerializer(serializers.ModelSerializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Room
        fields = ['id', 'name', 'user_ids', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_user_ids(self, value):
        if not value:
            raise serializers.ValidationError("É necessário pelo menos 1 usuário.")  # noqa: E501
        return list(set(value))  # remove duplicados

    def create(self, validated_data):
        request_user = self.context['request'].user
        user_ids = validated_data.pop('user_ids')
        user_ids.append(request_user.id)

        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.filter(id__in=user_ids)

        # Verificar se já existe uma sala privada com exatamente os mesmos usuários  # noqa: E501
        if users.count() == 2:
            existing_rooms = Room.objects.all()
            for room in existing_rooms:
                if set(room.users.values_list('id', flat=True)) == set(user_ids):  # noqa: E501
                    return room  # retorna a já existente

        room = Room.objects.create(name=validated_data.get('name'), owner=request_user)  # noqa: E501
        room.users.set(users)
        return room


class UserMiniSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']

    def get_avatar(self, obj):
        try:
            return obj.profile.avatar
        except AttributeError:
            return None


class LastMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'sender_id', 'sender_username', 'type_message', 'content', 'timestamp']  # noqa: E501


class RoomListSerializer(serializers.ModelSerializer):
    users = UserMiniSerializer(many=True)
    owner = UserMiniSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'name', 'owner', 'users', 'created_at', 'last_message']

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-timestamp').first()
        if last_msg:
            return LastMessageSerializer(last_msg).data
        return None
