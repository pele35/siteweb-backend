import pytest
from rest_framework.test import APIClient

from offers.factories.ad_placement_factory import AdvertisingPlacementDimensionFactory
from offers.factories.ad_placement_factory import AdvertisingPlacementFactory
from offers.factories.ad_placement_factory import FrontPageFactory
from offers.factories.offer_factories import AdvertisingPeriodFactory
from offers.factories.offer_factories import OfferFactory
from offers.factories.offer_factories import TimeSlotFactory
from offers.models import AdvertisingPeriod
from offers.models import CategoriesChoices
from offers.models import Offer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def offer_db(db):
    return Offer.objects.create(
        name="Offre Test",
        category=CategoriesChoices.AUDIO,
        is_active=True,
        price_ttc=100,
        price_ht=8000,
        tax_rate=20.0,
    )


@pytest.fixture
def offer(db):
    return OfferFactory()


@pytest.fixture
def timeslot(db):
    return TimeSlotFactory()


@pytest.fixture
def advertising_period(db):
    return AdvertisingPeriodFactory()


@pytest.fixture
def advertising_period_db(db):
    return AdvertisingPeriod.objects.create(
        name="Période Test", duration_days=5, discount_factor=0.9
    )


@pytest.fixture
def front_page(db):
    return FrontPageFactory()


@pytest.fixture
def advertising_placement(db):
    return AdvertisingPlacementFactory()


@pytest.fixture
def advertising_placement_dimension(db):
    return AdvertisingPlacementDimensionFactory()
