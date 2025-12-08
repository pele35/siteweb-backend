from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import JobOffer
from .serializers import JobOffersSerializers


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def job_offer(user):
    return JobOffer.objects.create(
        title="Développeur Python",
        description="Description test",
        department="Technique",
        type="CDI",
        location="Douala",
        posted_date=timezone.now().date(),
        username=user.username,
        is_urgent=True,
        draft=False,
    )


@pytest.mark.django_db
def test_slug_automatic_generation(job_offer):
    assert job_offer.slug_uri == "developpeur-python"


@pytest.mark.django_db
def test_is_expired_logic(job_offer):
    assert job_offer.is_expired() is False

    job_offer.posted_date = timezone.now().date() - timedelta(days=61)
    job_offer.save()

    assert job_offer.is_expired() is True


@pytest.mark.django_db
def test_list_job_offers(api_client, job_offer):
    url = reverse("carreer:job_list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    obs_list = response.context["paginated_data"]
    assert len(obs_list) == 1
    assert obs_list[0].title == job_offer.title


@pytest.mark.django_db
def test_filter_by_department(api_client, user):
    JobOffer.objects.create(
        title="Dev",
        department="Technique",
        posted_date=timezone.now().date(),
        username=user.username,
        type="CDI",
    )
    JobOffer.objects.create(
        title="RH",
        department="Editioral",
        posted_date=timezone.now().date(),
        username=user.username,
        type="CDI",
    )

    url = reverse("carreer:job_list")

    response = api_client.get(url, {"department": "Editioral"})

    jobs_list = response.context["paginated_data"]
    assert len(jobs_list) == 1

    assert jobs_list[0].title == "RH"


@pytest.mark.django_db
def test_filter_by_location(api_client, user):
    JobOffer.objects.create(
        title="Dev",
        location="Douala",
        posted_date=timezone.now().date(),
        username=user.username,
        type="CDI",
    )
    JobOffer.objects.create(
        title="RH",
        location="Yaounde",
        posted_date=timezone.now().date(),
        username=user.username,
        type="CDI",
    )

    url = reverse("carreer:job_list")

    response = api_client.get(url, {"location": "Yaounde"})

    jobs_list = response.context["paginated_data"]
    assert len(jobs_list) == 1

    assert jobs_list[0].location == "Yaounde"


@pytest.mark.django_db
def test_create_offer_future_date_invalid(user):
    future_date = timezone.now().date() + timedelta(days=10)

    data = {
        "title": "Future Job",
        "description": "...",
        "department": "Tech",
        "type": "CDI",
        "posted_date": future_date, 
        "username": user.username,
    }

    serializer = JobOffersSerializers(data=data)

    assert serializer.is_valid() is False
    assert "posted_date" in serializer.errors
    assert "Date de publication ne peut pas etre dans le futur." in str(
        serializer.errors["posted_date"]
    )
