from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat.models import Room

from .serializers import RoomCreateSerializer, RoomListSerializer


class CreateRoomAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RoomCreateSerializer(data=request.data, context={'request': request}) # noqa501
        if serializer.is_valid():
            room = serializer.save()
            return Response({
                "id": room.id,
                "name": room.name,
                "user_ids": list(room.users.values_list('id', flat=True)),
                "created_at": room.created_at
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListRoomsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = Room.objects.filter(users=request.user).prefetch_related("users", "messages") # noqa501
        serializer = RoomListSerializer(rooms, many=True)
        return Response(serializer.data)
