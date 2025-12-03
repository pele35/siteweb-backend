from django.contrib import admin

from tarifs.models import AdvertisingOffer
from tarifs.models import AdvertisingOption
from tarifs.models import Cart
from tarifs.models import CartItem
from tarifs.models import OfferCategory
from tarifs.models import OfferOption
from tarifs.models import Order
from tarifs.models import OrderItem
from tarifs.models import Placement


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    search_fields = ("user__username", "session_key")
    list_filter = ("created_at",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_amount", "created_at")
    search_fields = ("user__username",)
    list_filter = ("status", "created_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "unit_price")
    search_fields = ("order__id", "product__name")
    list_filter = ("order__status",)


admin.site.register(
    [Placement, AdvertisingOffer, AdvertisingOption, OfferCategory, OfferOption]
)
