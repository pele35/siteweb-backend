import random
from decimal import Decimal

import factory
from factory import Faker
from factory.django import DjangoModelFactory

from offers.models import AdvertisingPeriod
from offers.models import CategoriesChoices
from offers.models import Offer
from offers.models import OfferCharacteristic
from offers.models import OfferCharacteristicValue
from offers.models import TimeSlot


class OfferFactory(DjangoModelFactory):
    class Meta:
        model = Offer

    name = Faker("word")
    category = factory.Iterator(
        [
            CategoriesChoices.SITE,
            CategoriesChoices.AUDIO,
            CategoriesChoices.VIDEO,
            CategoriesChoices.POPUP,
            CategoriesChoices.PWA,
        ]
    )
    description = Faker("sentence")
    price_ht = factory.LazyFunction(lambda: Decimal(random.randint(100, 1000)))
    tax_rate = Decimal("19.25")
    is_active = True

    @factory.post_generation
    def update_price(obj, create, extracted, **kwargs):
        if create:
            obj.save()


class OfferCharacteristicFactory(DjangoModelFactory):
    class Meta:
        model = OfferCharacteristic

    category = factory.LazyFunction(
        lambda: random.choice(
            [
                CategoriesChoices.SITE,
                CategoriesChoices.AUDIO,
                CategoriesChoices.VIDEO,
                CategoriesChoices.POPUP,
                CategoriesChoices.PWA,
            ]
        )
    )
    name = Faker("word")
    value_type = factory.Iterator(
        [
            OfferCharacteristic.ValueType.STRING,
            OfferCharacteristic.ValueType.INTEGER,
            OfferCharacteristic.ValueType.BOOLEAN,
            OfferCharacteristic.ValueType.FLOAT,
        ]
    )


class OfferCharacteristicValueFactory(DjangoModelFactory):
    class Meta:
        model = OfferCharacteristicValue

    characteristic = factory.SubFactory(OfferCharacteristicFactory)
    offer = factory.SubFactory(OfferFactory)

    @factory.lazy_attribute
    def value(self):
        if self.characteristic.value_type == OfferCharacteristic.ValueType.STRING:
            return Faker("word").generate({})
        elif self.characteristic.value_type == OfferCharacteristic.ValueType.INTEGER:
            return str(random.randint(1, 100))
        elif self.characteristic.value_type == OfferCharacteristic.ValueType.BOOLEAN:
            return str(random.choice([True, False]))
        elif self.characteristic.value_type == OfferCharacteristic.ValueType.FLOAT:
            return str(round(random.uniform(1, 100), 2))
        return "N/A"


class TimeSlotFactory(DjangoModelFactory):
    class Meta:
        model = TimeSlot

    start_time = Faker("time_object")
    end_time = Faker("time_object")
    tax_augmentation = factory.LazyFunction(lambda: Decimal(random.randint(0, 30)))
    is_booked = factory.LazyFunction(lambda: random.choice([True, False]))

    @factory.post_generation
    def update_multiplier(obj, create, extracted, **kwargs):
        if create:
            obj.save()


class AdvertisingPeriodFactory(DjangoModelFactory):
    class Meta:
        model = AdvertisingPeriod

    name = Faker("word")
    duration_days = factory.LazyFunction(lambda: random.choice([7, 14, 30, 60, 90]))
    tax_reduction = factory.LazyFunction(lambda: Decimal(random.randint(0, 50)))

    @factory.post_generation
    def update_discount_factor(obj, create, extracted, **kwargs):
        if create:
            obj.save()
