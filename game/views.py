from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import EuroMillionMessage
from game.models import PlayerTicket
from game.models import ResultatEuromillion
from game.models import VideoEuroMillion
from game.serializers import EuroMillionMessageSerializer
from game.serializers import EuroMillionSerializer
from game.serializers import PlayerTicketSerializer
from game.serializers import ResultatEuromillionSerializer
from game.serializers import VideoEuroMillionSerializer
from game.service import bulk_send_email
from game.throttle import OncePerDayUserThrottle


class PlayEuroMillionView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = [OncePerDayUserThrottle]

    @swagger_auto_schema(
        operation_summary="Play Euro million",
        request_body=EuroMillionSerializer,
    )
    def post(self, request):
        serializer = EuroMillionSerializer(data=request.data)
        if serializer.is_valid():
            euromillion = serializer.save()
            bulk_send_email(
                numbers=euromillion.number_1_to_50,
                stars=euromillion.number_1_to_12,
                name=euromillion.name,
                surname=euromillion.surname,
                from_email=euromillion.email,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def throttled(self, request, wait):
        data = {
            "detail": "Only one EuroMillions play allowed per day. Please try again tomorrow.",
            "available_after": wait,
        }
        return Response(data, status=status.HTTP_429_TOO_MANY_REQUESTS)


class VideoEuroMillionView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_summary="Get Video EuroMillion")
    def get(self, request):
        instance = VideoEuroMillion.objects.first()
        if not instance:
            return Response(status=status.HTTP_200_OK)
        data = VideoEuroMillionSerializer(instance).data
        return Response(data, status=status.HTTP_200_OK)


class ResultatEuromillionListView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_summary="Get EuroMillions results")
    def get(self, request):
        queryset = ResultatEuromillion.objects.all()
        serializer = ResultatEuromillionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.generics import ListAPIView


class PlayerTicketListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = PlayerTicket.objects.all()
    serializer_class = PlayerTicketSerializer


class EuroMillionMessageView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_summary="Get EuroMillion message")
    def get(self, request):
        instance = EuroMillionMessage.objects.first()
        if not instance:
            return Response(status=status.HTTP_200_OK)
        data = EuroMillionMessageSerializer(instance).data
        return Response(data, status=status.HTTP_200_OK)
