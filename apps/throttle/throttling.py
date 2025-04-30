from rest_framework.throttling import UserRateThrottle


class CustomUserRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return None  # usa AnonRateThrottle

        return self.cache_format % {
            'scope': self.scope,
            'ident': request.user.pk
        }

    def get_rate(self):

        try:
            plan = self.request.user.profile.plan
        except Exception:
            plan = 'free'

        plan_rates = {
            'free': '50/minute',
            'pro': '200/minute',
            'admin': '500/minute'
        }

        return plan_rates.get(plan, '50/minute')
