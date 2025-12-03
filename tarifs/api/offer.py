from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from tarifs.models import AdvertisingOffer
from tarifs.models import OfferCategory
from tarifs.models import OfferOption
from tarifs.models import Placement
from tarifs.serializers import AdvertisingOfferSerializer
from tarifs.serializers import OfferCategorySerializer
from tarifs.serializers import OfferOptionSerializer
from tarifs.serializers import PlacementSerializer


class OfferCategoryViewSet(ModelViewSet):
    queryset = OfferCategory.objects.all()
    serializer_class = OfferCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


class AdvertisingOfferViewSet(ModelViewSet):
    queryset = AdvertisingOffer.objects.filter(is_active=True, is_visible=True)
    serializer_class = AdvertisingOfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "support_type"]

    @action(detail=True, methods=["get"])
    def options(self, request, pk=None):
        offer = self.get_object()
        options = offer.options.all()
        serializer = OfferOptionSerializer(options, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def placements(self, request, pk=None):
        offer = self.get_object()
        placements = offer.placements.all()
        serializer = PlacementSerializer(placements, many=True)
        return Response(serializer.data)


class OfferOptionViewSet(ModelViewSet):
    queryset = OfferOption.objects.all()
    serializer_class = OfferOptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["offer"]


class PlacementViewSet(ModelViewSet):
    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["offer", "available_slots"]


class OfferListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        offers = AdvertisingOffer.objects.filter(is_active=True, is_visible=True)
        serializer = AdvertisingOfferSerializer(offers, many=True)
        return Response(serializer.data)
