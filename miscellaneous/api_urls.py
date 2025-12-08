from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from miscellaneous.api import AboutViewSet
from miscellaneous.api import ContactAPIView
from miscellaneous.api import CookieViewSet
from miscellaneous.api import GeneralConditionViewSet
from miscellaneous.api import LegalNoticeViewSet
from miscellaneous.api import NewsletterConfirmationView
from miscellaneous.api import NewsletterSubscriptionView
from miscellaneous.api import PersonalDataViewSet
from miscellaneous.api import PublicityViewSet
from miscellaneous.api import ServiceViewSet
from miscellaneous.api import SliderViewSet
from miscellaneous.api import VideoViewSet

router = DefaultRouter()
router.register(r"about", AboutViewSet)
router.register(r"cookies", CookieViewSet)
router.register(r"personal-data", PersonalDataViewSet)
router.register(r"legal-notice", LegalNoticeViewSet)
router.register(r"general-conditions", GeneralConditionViewSet)
router.register(r"publicities", PublicityViewSet)
router.register(r"sliders", SliderViewSet)
router.register(r"videos", VideoViewSet)
router.register(r"services", ServiceViewSet, basename="service")

urlpatterns = [
    path("", include(router.urls)),
    path("contact/", ContactAPIView.as_view(), name="contact-api"),
    path("subscribe/", NewsletterSubscriptionView.as_view(), name="subscribe"),
    path(
        "newsletter/confirm/",
        NewsletterConfirmationView.as_view(),
        name="newsletter-confirm",
    ),
]
