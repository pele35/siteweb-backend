from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.META.get("PATH_INFO", "")
        maintenance_url = reverse("miscellaneous:maintenance")

        if (
            settings.MAINTENANCE_MODE
            and not path.startswith("/api/")
            and not path.startswith("/administration/")
            and not path.startswith("/static/")
            and path != maintenance_url
        ):
            return redirect(maintenance_url)
        return self.get_response(request)
