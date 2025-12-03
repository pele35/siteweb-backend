from django.contrib import admin

from offers.models import AdvertisingPeriod
from offers.models import AdvertisingPlacement
from offers.models import AdvertisingPlacementDimension
from offers.models import FrontPage
from offers.models import Offer
from offers.models import OfferCharacteristic
from offers.models import OfferCharacteristicValue
from offers.models import TimeSlot


class OfferCharacteristicInline(admin.TabularInline):
    model = OfferCharacteristicValue
    extra = 1
    readonly_fields = ("id",)
    fields = ("characteristic", "value")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price_ht",
        "price_ttc",
        "tax_rate",
        "is_active",
        "created_at",
    )
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("name", "category")
    list_per_page = 20
    inlines = [OfferCharacteristicInline]
    readonly_fields = ("id", "price_ttc", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "category", "description")}),
        ("Pricing", {"fields": ("price_ht", "tax_rate", "price_ttc")}),
        ("Status", {"fields": ("is_active",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(OfferCharacteristic)
class OfferCharacteristicAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "value_type")
    list_filter = ("name", "value_type")
    search_fields = ("name", "value_type")
    fieldsets = ((None, {"fields": ("name", "category", "value_type")}),)
    list_per_page = 20
    readonly_fields = ("id",)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = (
        "start_time",
        "end_time",
        "is_booked",
        "tax_augmentation",
        "multiplier",
    )
    list_filter = ("is_booked",)
    search_fields = ("start_time", "end_time")
    list_per_page = 20
    readonly_fields = ("id", "multiplier")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "start_time",
                    "end_time",
                    "is_booked",
                    "tax_augmentation",
                    "multiplier",
                )
            },
        ),
    )


@admin.register(AdvertisingPeriod)
class AdvertisingPeriodAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_days", "tax_reduction", "discount_factor")
    readonly_fields = ("id", "discount_factor")
    search_fields = ("name",)
    fieldsets = (
        (
            None,
            {"fields": ("name", "duration_days", "tax_reduction", "discount_factor")},
        ),
    )
    list_per_page = 20


@admin.register(OfferCharacteristicValue)
class OfferCharacteristicValueAdmin(admin.ModelAdmin):
    list_display = ("characteristic", "offer", "value")
    list_filter = ("characteristic", "offer")
    search_fields = ("characteristic__name", "offer__name", "value")
    fieldsets = ((None, {"fields": ("characteristic", "offer", "value")}),)
    list_per_page = 20
    readonly_fields = ("id",)


class AdvertisingPlacementDimensionInline(admin.TabularInline):
    model = AdvertisingPlacementDimension
    extra = 1
    fields = ("name", "width", "height", "is_active")
    min_num = 0
    can_delete = True
    show_change_link = True


@admin.register(AdvertisingPlacement)
class AdvertisingPlacementAdmin(admin.ModelAdmin):
    list_display = ("name", "front_page", "reference_id", "is_active")
    list_filter = ("is_active", "front_page")
    search_fields = ("name", "front_page__name", "reference_id")
    inlines = [AdvertisingPlacementDimensionInline]


@admin.register(FrontPage)
class FrontPageAdmin(admin.ModelAdmin):
    list_display = ("name", "path")
    search_fields = ("name", "path")


@admin.register(AdvertisingPlacementDimension)
class AdvertisingPlacementDimensionAdmin(admin.ModelAdmin):
    list_display = ("name", "advertising_placement", "width", "height", "is_active")
    list_filter = ("is_active", "advertising_placement")
    search_fields = ("name", "advertising_placement__name")
