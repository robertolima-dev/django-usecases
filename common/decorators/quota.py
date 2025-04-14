# common/decorators/quota.py

from functools import wraps

from rest_framework.exceptions import PermissionDenied

from apps.throttle.models import UserQuota


def check_quota(action):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            request = getattr(args[0], 'request', args[0])
            user = getattr(request, 'user', None)

            if not user or not user.is_authenticated:
                raise PermissionDenied("Usuário não autenticado.")

            quota = UserQuota.objects.filter(user=user, action=action).first() # noqa6501
            if not quota or quota.used >= quota.limit:
                raise PermissionDenied(f"Você atingiu o limite de uso para '{action}'.") # noqa6501

            return view_func(*args, **kwargs)
        return _wrapped_view
    return decorator
