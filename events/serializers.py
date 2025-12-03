from rest_framework import serializers

from events.models import Event
from events.models import EventType


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = "__all__"


class BookEventSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    tickets = serializers.IntegerField()

    def validate_tickets(self, value):
        if value <= 0:
            msg = "No tickets taken"
            raise serializers.ValidationError(msg)
        return value
