import datetime
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from offers.models import AdvertisingPlacement


@pytest.mark.django_db
def test_offer_list_view(api_client):
    url = reverse("offers")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_time_slot_list_view(api_client):
    url = reverse("time-slots")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_advertising_period_list_view(api_client):
    url = reverse("advertising-periods")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_offer_pricing_success(api_client, offer_db, timeslot, advertising_period_db):
    url = reverse("offer-price")
    timeslot.is_booked = False
    timeslot.save()
    today = datetime.date.today() 
    
    start_time = today + datetime.timedelta(days=7) 
    end_time = start_time + datetime.timedelta(days=5)
    data = {
        "offer_id": offer_db.id,
        "time_slot_id": timeslot.id,
        "start_time": start_time,
        "end_time": end_time,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    num_days = (end_time - start_time).days
    discount_factor = Decimal(advertising_period_db.discount_factor)
    expected_price = Decimal(offer_db.price_ttc) * num_days * discount_factor
    if not timeslot.is_booked:
        expected_price += (
            Decimal(offer_db.price_ttc)
            * num_days
            * (Decimal(timeslot.multiplier) - Decimal(1))
        )
    assert Decimal(response.data["offer_price"]).quantize(Decimal("0.01")) == Decimal(
        expected_price
    ).quantize(Decimal("0.01"))


@pytest.mark.django_db
def test_offer_pricing_start_time_today(api_client, offer, timeslot):
    url = reverse("offer-price")
    start_time = datetime.date.today()
    end_time = start_time + datetime.timedelta(days=2)
    start_time = start_time.isoformat()
    end_time = end_time.isoformat()
    data = {
        "offer_id": offer.id,
        "time_slot_id": timeslot.id,
        "start_time": start_time,
        "end_time": end_time,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "La date de debut doit etre supérieure à aujourd'hui." in str(response.data)


@pytest.mark.django_db
def test_offer_pricing_start_time_after_end_time(api_client, offer, timeslot):
    url = reverse("offer-price")
    timeslot.is_booked = False
    timeslot.save()
    start_time = datetime.date.today() + datetime.timedelta(days=5)
    end_time = datetime.date.today() + datetime.timedelta(days=2)
    data = {
        "offer_id": offer.id,
        "time_slot_id": timeslot.id,
        "start_time": start_time,
        "end_time": end_time,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "La date de début doit être antérieure à la date de fin." in str(
        response.data
    )


@pytest.mark.django_db
def test_time_slot_unavailable(api_client, offer, timeslot):
    timeslot.is_booked = True
    timeslot.save()
    url = reverse("offer-price")
    start_time = datetime.date.today() + datetime.timedelta(days=2)
    end_time = start_time + datetime.timedelta(days=5)
    data = {
        "offer_id": offer.id,
        "time_slot_id": timeslot.id,
        "start_time": start_time,
        "end_time": end_time,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Créneau horaire non valide ou déjà réservé." in str(response.data)


@pytest.mark.django_db
def test_list_all_active_advertising_placements(
    api_client, front_page, advertising_placement, advertising_placement_dimension
):
    AdvertisingPlacement.objects.all().delete()

    advertising_placement.front_page = front_page
    advertising_placement.is_active = True
    advertising_placement.save()
    advertising_placement_dimension.advertising_placement = advertising_placement
    advertising_placement_dimension.save()

    url = reverse("advertising-placements-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert "dimensions" in response.data[0]
    assert response.data[0]["is_active"] is True


@pytest.mark.django_db
def test_list_advertising_placements_by_frontpage_success(
    api_client, front_page, advertising_placement, advertising_placement_dimension
):
    advertising_placement.front_page = front_page
    advertising_placement.save()
    advertising_placement_dimension.advertising_placement = advertising_placement
    advertising_placement_dimension.save()

    url = reverse("advertising-placements-list")
    response = api_client.get(url, {"path": front_page.path})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == advertising_placement.name
    assert "dimensions" in response.data[0]


@pytest.mark.django_db
def test_list_advertising_placements_by_frontpage_no_results(
    api_client, front_page, advertising_placement
):
    advertising_placement.front_page = front_page
    advertising_placement.save()

    url = reverse("advertising-placements-list")
    response = api_client.get(url, {"path": "/inexistant"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []
