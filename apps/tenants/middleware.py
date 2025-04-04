from django.utils.deprecation import MiddlewareMixin

# from apps.tenants.models import Tenant


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user

        if user.is_authenticated:
            tenants = user.tenants.all()
            if tenants.exists():
                request.tenant = tenants.first()
            else:
                request.tenant = None
        else:
            request.tenant = None
