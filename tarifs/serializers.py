from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from tarifs.models import AdvertisingOffer
from tarifs.models import AdvertisingOption
from tarifs.models import Cart
from tarifs.models import CartItem
from tarifs.models import OfferCategory
from tarifs.models import OfferOption
from tarifs.models import Order
from tarifs.models import OrderItem
from tarifs.models import Placement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Identifiants incorrects")


class OfferCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferCategory
        fields = "__all__"


class OfferOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferOption
        fields = "__all__"


class PlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placement
        fields = "__all__"


class AdvertisingOfferSerializer(serializers.ModelSerializer):
    category = OfferCategorySerializer(read_only=True)
    options = OfferOptionSerializer(many=True, read_only=True)
    placements = PlacementSerializer(many=True, read_only=True)

    support_type_display = serializers.CharField(
        source="get_support_type_display", read_only=True
    )

    class Meta:
        model = AdvertisingOffer
        fields = "__all__"
        extra_fields = ["support_type_display"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisingOffer
        fields = ["id", "start_date", "end_date", "audio_durations"]


class AdvertisingOptionSerializer(serializers.ModelSerializer):
    offer_id = serializers.IntegerField(source="offer.id", read_only=True)

    class Meta:
        model = AdvertisingOption
        fields = ["id", "offer_id", "start_date", "end_date", "time_slot"]
        read_only_fields = ["id"]


class CartItemSerializer(serializers.ModelSerializer):
    product = AdvertisingOptionSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items"]


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "unit_price",
            "total_price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "status", "total_amount", "created_at", "items"]
