from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer

from offers.models import AdvertisingPeriod
from offers.models import AdvertisingPlacement
from offers.models import AdvertisingPlacementDimension
from offers.models import CategoriesChoices
from offers.models import FrontPage
from offers.models import Offer
from offers.models import OfferCharacteristic
from offers.models import OfferCharacteristicValue
from offers.models import TimeSlot
from offers.repositories.offer_repository import OfferRepository


class OfferCharacteristicSerializer(ModelSerializer):
    class Meta:
        model = OfferCharacteristic
        fields = ["name", "value_type"]


class OfferCharacteristicValueSerializer(ModelSerializer):
    characteristic = OfferCharacteristicSerializer()

    class Meta:
        model = OfferCharacteristicValue
        fields = ["characteristic", "value"]


class OfferSerializer(ModelSerializer):
    category_label = serializers.CharField(
        source="get_category_display", read_only=True
    )
    characteristic_values = OfferCharacteristicValueSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Offer
        fields = [
            "id",
            "name",
            "category",
            "category_label",
            "description",
            "price_ht",
            "price_ttc",
            "tax_rate",
            "is_active",
            "characteristic_values",
        ]


class TimeSlotSerializer(ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = [
            "id",
            "start_time",
            "end_time",
            "tax_augmentation",
            "multiplier",
        ]


class AdvertisingPeriodSerializer(ModelSerializer):
    class Meta:
        model = AdvertisingPeriod
        fields = ["id", "name", "duration_days", "tax_reduction", "discount_factor"]


class OfferPricingSerializer(Serializer):
    offer_id = serializers.IntegerField()
    start_time = serializers.DateField()
    end_time = serializers.DateField()
    time_slot_id = serializers.IntegerField(required=False)

    def validate_offer_id(self, value):
        if not OfferRepository.verify_offer_existance(offer_id=value):
            raise serializers.ValidationError(_("Offre non valide ou inactive."))
        return value

    def validate_time_slot_id(self, value):
        if not OfferRepository.verify_time_slot_disponibility(time_slot_id=value):
            raise serializers.ValidationError(
                _("Créneau horaire non valide ou déjà réservé.")
            )
        return value

    def validate_start_time(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError(
                _("La date de debut doit etre supérieure à aujourd'hui.")
            )
        return value

    def validate(self, attrs):
        if attrs["start_time"] >= attrs["end_time"]:
            raise serializers.ValidationError(
                _("La date de début doit être antérieure à la date de fin.")
            )
        offer = OfferRepository.get_offer_by_id(attrs["offer_id"])
        if offer.category == CategoriesChoices.AUDIO and "time_slot_id" not in attrs:
            raise serializers.ValidationError(
                _(
                    "Le créneau horaire est obligatoire pour les offres de type audiovisuel."
                )
            )
        return attrs


class AdvertisingPlacementDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisingPlacementDimension
        fields = ["id", "name", "width", "height", "is_active"]


class AdvertisingPlacementSerializer(serializers.ModelSerializer):
    dimensions = AdvertisingPlacementDimensionSerializer(many=True, read_only=True)

    class Meta:
        model = AdvertisingPlacement
        fields = [
            "id",
            "name",
            "reference_id",
            "description",
            "is_active",
            "dimensions",
        ]


class FrontPageSerializer(serializers.ModelSerializer):
    advertising_placements = AdvertisingPlacementSerializer(many=True, read_only=True)

    class Meta:
        model = FrontPage
        fields = ["id", "name", "path", "advertising_placements"]
