from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.presence.models import UserPresence

from .serializers import OnlineUserSerializer

User = get_user_model()


class OnlineUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users_online_ids = UserPresence.objects.filter(is_online=True).values_list("user_id", flat=True) # noqa501
        users = User.objects.filter(id__in=users_online_ids)
        serializer = OnlineUserSerializer(users, many=True)
        return Response(serializer.data)
