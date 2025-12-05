from rest_framework import serializers

from .models import JobOffer


class JobOffersSerializers(serializers.ModelSerializer):
    is_expired_api = serializers.BooleanField(source="is_expired", read_only=True)
    days_since_posted_field = serializers.IntegerField(
        source="days_since_posted", read_only=True
    )

    class Meta:
        model = JobOffer
        fields = [
            "id",
            "title",
            "slug_uri",
            "description",
            "department",
            "type",
            "location",
            "experience",
            "posted_date",
            "is_urgent",
            "requirements",
            "benefits",
            "days_since_posted_field",
            "is_expired_api",
            "created_at",
        ]

    def validate_posted_date(self, value):
        from django.utils import timezone

        if value > timezone.now().date():
            raise serializers.ValidationError(
                "Date de publication ne peut pas etre dans le futur."
            )
        return value
