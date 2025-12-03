from rest_framework import serializers

from emission.models import Emission
from emission.models import FridayEditorial
from emission.models import PodcastHoroscope
from emission.models import SubEmission


class EmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emission
        fields = "__all__"


class SubEmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubEmission
        fields = "__all__"


class FridayEditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridayEditorial
        fields = "__all__"


class PodcastHoroscopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastHoroscope
        fields = "__all__"
