from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import JobOffer
from .serializers import JobOfferSerializer

class JobOfferViewSet(ModelViewSet):
    queryset = JobOffer.objects.all().order_by('posted_date')
    serializer_class = JobOfferSerializer