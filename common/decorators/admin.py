import logging
from functools import wraps

from django.contrib import messages

logger = logging.getLogger(__name__)


def admin_action_log(message_template=None):
    """
    Registra no terminal/log + mensagem no painel admin após execução de uma action. # noqa501
    """
    def decorator(func):
        @wraps(func)
        def wrapper(modeladmin, request, queryset):
            count = queryset.count()
            message = message_template or f"Ação '{func.__name__}' aplicada em {count} item(ns)" # noqa501

            logger.info(f"[ADMIN ACTION] {func.__name__} - {count} registro(s) | Usuário: {request.user}") # noqa501
            messages.success(request, message)

            return func(modeladmin, request, queryset)
        return wrapper
    return decorator
