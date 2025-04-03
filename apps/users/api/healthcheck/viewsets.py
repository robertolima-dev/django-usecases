from django.http import JsonResponse
from rest_framework.views import APIView


class HealthcheckViewSet(APIView):
    http_method_names = ['get', ]
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def get(self, request):
        return JsonResponse({'status': 'ok'})
