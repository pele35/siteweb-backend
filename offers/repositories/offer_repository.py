from offers.models import AdvertisingPeriod
from offers.models import Offer
from offers.models import TimeSlot


class OfferRepository:
    @staticmethod
    def get_active_offers():
        return Offer.objects.filter(is_active=True)

    @staticmethod
    def get_all_offers():
        return Offer.objects.all()

    @staticmethod
    def get_offer_by_id(offer_id):
        return Offer.objects.filter(id=offer_id, is_active=True).first()

    @staticmethod
    def verify_offer_existance(offer_id):
        return Offer.objects.filter(id=offer_id, is_active=True).exists()

    @staticmethod
    def get_all_time_slots():
        return TimeSlot.objects.all()

    @staticmethod
    def get_time_slot_by_id(time_slot_id):
        return TimeSlot.objects.filter(id=time_slot_id).first()

    @staticmethod
    def verify_time_slot_disponibility(time_slot_id):
        return TimeSlot.objects.filter(id=time_slot_id, is_booked=False).exists()

    @staticmethod
    def get_advertising_periods():
        return AdvertisingPeriod.objects.all()

    @staticmethod
    def get_advertising_period_by_id(advertising_period_id):
        return AdvertisingPeriod.objects.filter(id=advertising_period_id).first()

    @staticmethod
    def get_discount_factor_for_days(num_days):
        period = (
            AdvertisingPeriod.objects.filter(duration_days__lte=num_days)
            .order_by("-duration_days")
            .first()
        )
        return period.discount_factor if period else 1.0
