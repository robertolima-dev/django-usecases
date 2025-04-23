from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.permissions.permissions import IsAdmin, IsSupport, IsUser


@extend_schema(
    tags=["Permissions"]
)
class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Você é um admin!"})


@extend_schema(
    tags=["Permissions"]
)
class UserOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        return Response({"message": "Você é um user!"})


@extend_schema(
    tags=["Permissions"]
)
class SupportOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsSupport]

    def get(self, request):
        return Response({"message": "Você é um support!"})
