from rest_framework.routers import DefaultRouter

from carreer.views import JobOfferViewSet

router = DefaultRouter()
router.register(r"joboffers", JobOfferViewSet, basename="jobs")

urlpatterns = router.urls