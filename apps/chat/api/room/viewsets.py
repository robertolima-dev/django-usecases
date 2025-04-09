from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat.models import Room

from .serializers import RoomSerializer

User = get_user_model()


class CreateOrGetRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user1 = request.user
        user2_id = request.data.get('user2_id')

        if not user2_id:
            return Response({"detail": "user2_id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST) # noqa501

        try:
            user2 = User.objects.get(id=user2_id)
        except User.DoesNotExist:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND) # noqa501

        # Ordena por id para manter consistência
        u1, u2 = sorted([user1, user2], key=lambda u: u.id)

        room, created = Room.objects.get_or_create(user1=u1, user2=u2)
        serializer = RoomSerializer(room)

        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK) # noqa501
