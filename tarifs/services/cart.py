from typing import Any
from typing import Callable
from typing import Type
from typing import Union

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.serializers import Serializer

from tarifs.models import AdvertisingOffer
from tarifs.models import AdvertisingOption
from tarifs.models import Cart
from tarifs.models import CartItem
from tarifs.models import Order
from tarifs.models import OrderItem
from tarifs.models import OrderUserInformation


class CartService:
    def __init__(
        self,
        user: User = None,
        serializer: Union[Type[Serializer], Callable[..., Serializer]] = None,
    ):
        self.user: User = user
        self.serializer = serializer
        self.error = None

    def _get_or_create_cart(self) -> Cart:
        cart, _ = Cart.objects.get_or_create(user=self.user)
        return cart

    def _get_serialized_data(self, object) -> dict[str, Any]:
        return self.serializer(object).data

    def _add_item(self, data: dict) -> tuple[Cart, dict]:
        cart = self._get_or_create_cart()
        product_id = data.get("offer_id")
        quantity = data.get("quantity", 1)
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        time_slot = data.get("time_slot", None)

        if not product_id or not quantity:
            self.error = {
                "detail": "Product ID and quantity are required.",
                "status": status.HTTP_400_BAD_REQUEST,
            }

        product = get_object_or_404(AdvertisingOffer, id=product_id)
        offer_option, created = AdvertisingOption.objects.get_or_create(
            offer=product, user=self.user
        )

        item, created = CartItem.objects.get_or_create(cart=cart, product=offer_option)
        if not created:
            item.quantity += int(quantity)
        else:
            offer_option.start_date = start_date
            offer_option.end_date = end_date
            offer_option.time_slot = time_slot
            offer_option.save()
            item.quantity = int(quantity)
            item.product = offer_option
        item.save()
        return cart, self.error

    def _update_cart_item(
        self, item_id: int, data: dict[str, int]
    ) -> tuple[CartItem, dict[str, Union[str, int]]]:
        cart = self._get_or_create_cart()
        item = get_object_or_404(CartItem, product__offer__id=item_id, cart=cart)
        quantity = data.get("quantity")
        if quantity:
            try:
                item.quantity = int(quantity)
                item.save()
            except ValueError:
                self.error = {
                    "detail": "Invalid quantity.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
        return item, self.error

    def _remove_cart_item(self, item_id: int) -> dict:
        cart = self._get_or_create_cart()
        item = get_object_or_404(CartItem, product__offer__id=item_id, cart=cart)
        item.delete()
        serialized_data = self._get_serialized_data(cart)
        return serialized_data

    @transaction.atomic
    def _synchronized_cart(self, data: dict) -> tuple[Cart, dict]:
        cart = self._get_or_create_cart()
        items = data.get("items", [])
        if not isinstance(items, list):
            self.error = {
                "detail": "Invalid items format.",
                "status": status.HTTP_400_BAD_REQUEST,
            }

        AdvertisingOption.objects.filter(cart_items__cart=cart).delete()
        cart.items.all().delete()
        for item_data in items:
            product_id = item_data.get("offer_id")
            quantity = item_data.get("quantity", 1)
            start_date = item_data.get("start_date")
            end_date = item_data.get("end_date")
            time_slot = item_data.get("time_slot", None)
            if not product_id or not isinstance(quantity, int) or quantity < 1:
                self.error = {
                    "detail": "Invalid product ID or quantity.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            if start_date and end_date and start_date > end_date:
                self.error = {
                    "detail": "Start date must be before end date.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }

            product = get_object_or_404(AdvertisingOffer, id=product_id)
            offer_option, _ = AdvertisingOption.objects.get_or_create(
                user=self.user,
                offer=product,
                start_date=start_date,
                end_date=end_date,
                time_slot=time_slot,
            )
            CartItem.objects.create(cart=cart, product=offer_option, quantity=quantity)

        return cart, self.error

    @transaction.atomic
    def _checkout_cart(self, data: dict) -> tuple[Order, dict]:
        cart = self._get_or_create_cart()
        if not cart.items.exists():
            self.error = {
                "detail": "Panier vide.",
                "status": status.HTTP_400_BAD_REQUEST,
            }

        total = sum(
            [
                item.product.offer.unit_price * item.quantity
                for item in cart.items.select_related("product__offer")
            ]
        )
        if total <= 0:
            self.error = {
                "detail": "Le montant total doit etre superieur à zero",
                "status": status.HTTP_400_BAD_REQUEST,
            }

        enterprise_name = data.get("company")
        address = data.get("address")
        city = data.get("city")
        postal_code = data.get("postal_code")
        country = data.get("country")
        if not enterprise_name or not address or not city or not postal_code:
            self.error = {
                "detail": "Toutes les infos sont de l'entreprise sont nécessaires",
                "status": status.HTTP_400_BAD_REQUEST,
            }

        user_info = OrderUserInformation.objects.create(
            enterprise_name=enterprise_name,
            address=address,
            city=city,
            postal_code=postal_code,
            country=country,
        )

        order = Order.objects.create(
            user=cart.user,
            total_amount=total,
            other_information=user_info,
        )

        order_items = [
            OrderItem(
                order=order,
                product=cart_item.product.offer,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.offer.unit_price,
            )
            for cart_item in cart.items.select_related("product__offer")
        ]
        OrderItem.objects.bulk_create(order_items)
        cart.items.all().delete()
        return order, self.error
