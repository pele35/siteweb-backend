from rest_framework import serializers
from .models import JobOffer
from django.utils import timezone

class JobOffersSerializers(serializers.ModelSerializer):
    is_expired = serializers.IntegerField(source='is_expired',read_only=True)
    days_since_posted=serializers.IntegerField(source='days_since_posted',read_only=True)

    class Meta :
        model= JobOffer
        fields = [
            'id', 'title', 'slug_uri', 'description', 'department', 
            'type', 'location', 'experience', 'posted_date', 
            'is_urgent', 'requirements', 'benefits', 
            'days_ago', 'is_expired', 'created_at'
        ]
        
        def validate_post_date(self,value):
            if value < timezone.now().date():
                raise serializers.ValidationError('Date de publication ne peut pas etre dans le passe')
            return value