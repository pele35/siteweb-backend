from decimal import Decimal

from offers.models import CategoriesChoices
from offers.repositories.offer_repository import OfferRepository


class OfferService:
    @staticmethod
    def list_active_offers():
        return OfferRepository.get_active_offers()

    @staticmethod
    def list_all_offers():
        return OfferRepository.get_all_offers()

    @staticmethod
    def list_time_slots():
        return OfferRepository.get_all_time_slots()

    @staticmethod
    def list_advertising_periods():
        return OfferRepository.get_advertising_periods()

    @staticmethod
    def calculate_offer_price(data):
        offer = OfferRepository.get_offer_by_id(data["offer_id"])
        offer_price_ttc = offer.price_ttc
        num_days = (data["end_time"] - data["start_time"]).days
        time_slot_id = data.get("time_slot_id")
        time_slot = None
        if time_slot_id:
            time_slot = OfferRepository.get_time_slot_by_id(time_slot_id)
        discount_factor = Decimal(
            OfferRepository.get_discount_factor_for_days(num_days)
        )
        total_price = offer_price_ttc * num_days * discount_factor
        is_time_slot_valid = (
            time_slot_id is not None
            and time_slot is not None
            and OfferRepository.verify_time_slot_disponibility(time_slot_id)
        )
        if offer.category == CategoriesChoices.AUDIO and is_time_slot_valid:
            total_price += (
                offer_price_ttc
                * num_days
                * (Decimal(time_slot.multiplier) - Decimal(1))
            )
        return Decimal(total_price)
