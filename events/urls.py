from rest_framework.routers import DefaultRouter

from events.views import EventViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")

urlpatterns = router.urls
