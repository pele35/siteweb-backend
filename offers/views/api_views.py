from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from offers.serializers import AdvertisingPeriodSerializer
from offers.serializers import AdvertisingPlacementSerializer
from offers.serializers import OfferPricingSerializer
from offers.serializers import OfferSerializer
from offers.serializers import TimeSlotSerializer
from offers.services.ad_placement_service import AdPlacementService
from offers.services.offer_service import OfferService


class OfferListView(ListAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        return OfferService.list_active_offers()


class TimeSlotListView(ListAPIView):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        return OfferService.list_time_slots()


class AdvertisingPeriodListView(ListAPIView):
    serializer_class = AdvertisingPeriodSerializer

    def get_queryset(self):
        return OfferService.list_advertising_periods()


class OfferPricingCalculationView(APIView):
    @swagger_auto_schema(
        request_body=OfferPricingSerializer,
        responses={
            200: openapi.Response(""),
            400: openapi.Response("Erreur de validation"),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = OfferPricingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        offer_price = OfferService.calculate_offer_price(serializer.validated_data)
        return Response(data={"offer_price": offer_price}, status=status.HTTP_200_OK)


class AdvertisingPlacementAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Retourne les emplacements publicitaires actifs. Si `path` fourni, filtre par frontpage.",
        manual_parameters=[
            openapi.Parameter(
                "path",
                openapi.IN_QUERY,
                description="Chemin de la page (Optionnel). Si fourni, filtre les emplacements publicitaires pour cette page.",
                type=openapi.TYPE_STRING,
                required=False,
                example="/homepage",
            ),
        ],
        responses={
            200: AdvertisingPlacementSerializer(many=True),
        },
    )
    def get(self, request):
        frontpage_path = self._get_frontpage_path(request)
        if frontpage_path is None:
            placements = self._list_all()
            return self._respond(placements)

        placements = self._list_by_frontpage(frontpage_path)
        return self._respond(placements)

    @staticmethod
    def _get_frontpage_path(request):
        return request.query_params.get("path")

    @staticmethod
    def _list_all():
        return AdPlacementService.list_active_advertising_placements()

    @staticmethod
    def _list_by_frontpage(path):
        return AdPlacementService.list_active_advertising_placements_by_frontpage(path)

    @staticmethod
    def _respond(placements):
        serializer = AdvertisingPlacementSerializer(placements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
