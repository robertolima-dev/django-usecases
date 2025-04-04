# permissions/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.permissions.permissions import IsAdmin, IsSupport, IsUser


class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Você é um admin!"})


class UserOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        return Response({"message": "Você é um user!"})


class SupportOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsSupport]

    def get(self, request):
        return Response({"message": "Você é um support!"})
