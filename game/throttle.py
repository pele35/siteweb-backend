from django.core.cache import cache
from django.utils import timezone
from rest_framework.throttling import BaseThrottle


class OncePerDayUserThrottle(BaseThrottle):
    """
    Custom throttle to limit users to one request per day
    """

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        today = timezone.now().date().isoformat()
        return f"throttle_once_per_day_{ident}_{today}"

    def allow_request(self, request, view):
        key = self.get_cache_key(request, view)
        if cache.get(key):
            return False
        cache.set(key, True, timeout=60 * 60 * 24)
        return True

    def wait(self):
        now = timezone.now()
        tomorrow = now.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + timezone.timedelta(days=1)
        return (tomorrow - now).total_seconds()
