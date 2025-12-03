from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import Event
from events.serializers import BookEventSerializer
from events.serializers import EventSerializer


class EventViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Event.objects.filter(status=True)
    serializer_class = EventSerializer

    @action(
        detail=True,
        methods=["post"],
        url_path="book",
        serializer_class=BookEventSerializer,
    )
    def book(self, request, pk=None):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        request_tickets = serializer.validated_data["tickets"]

        event = self.get_object()
        if event.remaining_places <= 0:
            return Response(
                {"detail": "No more places available."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request_tickets >= event.remaining_places:
            event.tickets -= request_tickets
            event.save()
        else:
            Response(
                {"detail": "Cannot book more than available place"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "places booked successfully"}, status=status.HTTP_200_OK
        )
