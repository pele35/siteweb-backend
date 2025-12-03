from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from tarifs.api.auth import CookieTokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="MLVM API Documentation",
        default_version="v1",
        description="API pour la gestion des offres publicitaires et paiements",
        contact=openapi.Contact(email="contact@ekila.com"),
        license=openapi.License(name="License Propriétaire"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("administration/", admin.site.urls),
    path("actualites/", include("actuality.urls")),
    path("emission/", include("emission.urls")),
    path("carreer/", include("carreer.urls")),
    path("", include("miscellaneous.urls")),
    path("api/", include("actuality.api_urls")),
    path("api/euro-million/", include("game.urls")),
    path("api/events/", include("events.urls")),
    path("api/miscellaneous/", include("miscellaneous.api_urls")),
    path("api/", include("emission.api_urls")),
    path("api/tarif/", include("tarifs.urls")),
    path("api/offers/", include("offers.urls.api_urls")),
    path("api/", include("carreer.api_urls")),
    path(
        "api/docs/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui",
    ),
    path("api/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/docs/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "MNLV Administration"
admin.site.site_title = "MNLV Administration"
admin.site.index_title = "MNLV Website Dashboard"
