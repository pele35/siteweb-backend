import random

import factory
from factory.django import DjangoModelFactory

from offers.models import AdvertisingPlacement
from offers.models import AdvertisingPlacementDimension
from offers.models import FrontPage


class FrontPageFactory(DjangoModelFactory):
    class Meta:
        model = FrontPage

    name = factory.Faker("word")
    path = factory.Faker("uri_path")


class AdvertisingPlacementFactory(DjangoModelFactory):
    class Meta:
        model = AdvertisingPlacement

    name = factory.Faker("word")
    reference_id = factory.Sequence(lambda n: f"ad{n:03d}")
    front_page = factory.SubFactory(FrontPageFactory)
    is_active = True


class AdvertisingPlacementDimensionFactory(DjangoModelFactory):
    class Meta:
        model = AdvertisingPlacementDimension

    advertising_placement = factory.SubFactory(AdvertisingPlacementFactory)
    name = factory.Faker("word")
    width = factory.LazyFunction(lambda: random.randint(100, 1000))
    height = factory.LazyFunction(lambda: random.randint(50, 500))
