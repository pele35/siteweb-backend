from django.db import transaction
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tarifs.serializers import CartItemSerializer
from tarifs.serializers import CartSerializer
from tarifs.serializers import OrderSerializer
from tarifs.services.cart import CartService


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_service = CartService(user=request.user, serializer=CartSerializer)
        cart = cart_service._get_or_create_cart()
        serializer_data = cart_service._get_serialized_data(cart)
        return Response(serializer_data)


class CartAddItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_service = CartService(user=request.user, serializer=CartSerializer)
        cart, error_reponse = cart_service._add_item(data=request.data)
        if error_reponse:
            return Response(
                {"detail": error_reponse["detail"]}, status=error_reponse["status"]
            )
        serialized_data = cart_service._get_serialized_data(cart)
        return Response(serialized_data, status=status.HTTP_201_CREATED)


class CartUpdateItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, item_id):
        cart_service = CartService(user=request.user, serializer=CartItemSerializer)
        item, error_reponse = cart_service._update_cart_item(
            item_id=item_id, data=request.data
        )
        if error_reponse:
            return Response(
                {"detail": error_reponse["detail"]}, status=error_reponse["status"]
            )
        serialized_data = cart_service._get_serialized_data(item)
        return Response(serialized_data)


class CartRemoveItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, item_id):
        cart_service = CartService(user=request.user, serializer=CartSerializer)
        serialized_data = cart_service._remove_cart_item(item_id=item_id)
        return Response(serialized_data)


class CartSyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart_service = CartService(user=request.user, serializer=CartSerializer)
        cart, error_reponse = cart_service._update_cart_item(data=request.data)
        if error_reponse:
            return Response(
                {"detail": error_reponse["detail"]}, status=error_reponse["status"]
            )
        serialized_data = cart_service._get_serialized_data(cart)
        return Response(serialized_data, status=status.HTTP_200_OK)


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_service = CartService(user=request.user, serializer=OrderSerializer)
        order, error_reponse = cart_service._checkout_cart(data=request.data)
        if error_reponse:
            return Response(
                {"detail": error_reponse["detail"]}, status=error_reponse["status"]
            )
        serialized_data = cart_service._get_serialized_data(order)
        return Response(serialized_data, status=status.HTTP_201_CREATED)
