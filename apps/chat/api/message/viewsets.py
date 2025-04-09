from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat.models import Message, Room

from .serializers import MessageCreateSerializer, MessageSerializer


class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MessageCreateSerializer(data=request.data, context={'request': request}) # noqa501
        if serializer.is_valid():
            message = serializer.save()

            # (Opcional) Enviar via WebSocket também
            from asgiref.sync import async_to_sync
            from channels.layers import get_channel_layer

            channel_layer = get_channel_layer()
            room_group_name = f"private_chat_room_{message.room.id}"
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    "type": "chat_message",
                    "message": message.content,
                    "sender_id": message.sender.id,
                    "sender_username": message.sender.username,
                    "timestamp": str(message.timestamp)
                }
            )

            return Response({"detail": "Mensagem enviada com sucesso."}, status=status.HTTP_201_CREATED) # noqa501

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        room_id = request.query_params.get("room_id")

        if not room_id:
            return Response({"detail": "Parâmetro 'room_id' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST) # noqa501

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"detail": "Sala não encontrada."}, status=status.HTTP_404_NOT_FOUND) # noqa501

        if request.user != room.user1 and request.user != room.user2:
            return Response({"detail": "Você não faz parte desta sala."}, status=status.HTTP_403_FORBIDDEN) # noqa501

        messages = Message.objects.filter(room=room).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
