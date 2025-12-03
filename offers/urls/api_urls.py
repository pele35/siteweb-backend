from django.urls import path

from offers.views.api_views import AdvertisingPeriodListView
from offers.views.api_views import AdvertisingPlacementAPIView
from offers.views.api_views import OfferListView
from offers.views.api_views import OfferPricingCalculationView
from offers.views.api_views import TimeSlotListView


urlpatterns = [
    path("", OfferListView.as_view(), name="offers"),
    path("time-slots", TimeSlotListView.as_view(), name="time-slots"),
    path(
        "advertising-periods",
        AdvertisingPeriodListView.as_view(),
        name="advertising-periods",
    ),
    path("price", OfferPricingCalculationView.as_view(), name="offer-price"),
    path(
        "advertising-placements",
        AdvertisingPlacementAPIView.as_view(),
        name="advertising-placements-list",
    ),
]
