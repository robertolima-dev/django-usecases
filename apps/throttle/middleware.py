from django.core.exceptions import PermissionDenied
# from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

from .utils import check_and_increment_quota

# Mapear rotas e ações que precisam de limitação
LIMITED_ROUTES = {
    "/api/v1/uploads/": "upload",
    # Adicione outras rotas e ações conforme necessário
}


class QuotaMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return None

        path = request.path_info
        action = LIMITED_ROUTES.get(path)

        # Se não está mapeado, ignora
        if not action:
            return None

        try:
            check_and_increment_quota(request.user, action)
        except PermissionDenied as e:
            from django.http import JsonResponse
            return JsonResponse(
                {"detail": str(e)},
                status=429  # HTTP 429 Too Many Requests
            )
