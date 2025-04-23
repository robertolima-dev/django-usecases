from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView


@extend_schema(
    tags=["Health Check"]
)
class HealthcheckViewSet(APIView):
    http_method_names = ['get', ]
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def get(self, request):
        return JsonResponse({'status': 'ok'})
