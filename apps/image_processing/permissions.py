from rest_framework.permissions import BasePermission


class IsSqsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token and token.startswith('Token '):
            token_value = token.split(' ')[1]
            if token_value == '1234':
                return True

        return False
