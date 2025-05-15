from django.conf import settings
from rest_framework.permissions import BasePermission


class IsSqsAuthenticated(BasePermission):
    def has_permission(self, request, view):

        token = request.META.get('HTTP_AUTHORIZATION', None)

        if token and token.startswith('Token '):
            token_value = token.split(' ')[1].strip()

            if token_value == str(settings.APP_KEY):
                return True

        return False
