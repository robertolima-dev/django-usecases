from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


class DashboardBroadcastView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        data = request.data  # Ex: {"metric": "new_users", "value": 3}
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "dashboard",
            {
                "type": "dashboard_update",
                "data": data
            }
        )
        return Response({"detail": "Mensagem enviada para o dashboard!"})
