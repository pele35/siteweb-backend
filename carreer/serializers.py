from rest_framework import serializers
from .models import JobOffer

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = "__all__"
        read_only_fields= ['posted_date']
    