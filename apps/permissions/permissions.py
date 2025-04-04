from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, "profile") and
            request.user.profile.access_level == "admin"
        )


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, "profile") and
            request.user.profile.access_level == "user"
        )


class IsSupport(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, "profile") and
            request.user.profile.access_level == "support"
        )
