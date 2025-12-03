from typing import Union

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status

from tarifs.models import Order


def init_cinetpay(*, order_id: int, user: User) -> tuple[dict[str, Union[str, int]]]:
    error = None
    order = get_object_or_404(Order, id=order_id, user=user)
    if not order.code_verified:
        error = {
            "detail": "Vérification email requise.",
            "status": status.HTTP_403_FORBIDDEN,
        }

    data = {
        "apikey": settings.CINETPAY_API_KEY,
        "site_id": settings.CINETPAY_SITE_ID,
        "transaction_id": str(order.id),
        "amount": int(order.total_amount),
        "currency": "XAF",
        "channels": "ALL",
        "description": f"Paiement commande {order.id}",
        "return_url": settings.CINETPAY_RETURN_URL,
        "notify_url": settings.CINETPAY_NOTIFY_URL,
    }
    response = requests.post("https://api-checkout.cinetpay.com/v2/payment", json=data)
    if response.status_code != 200:
        error = {
            "detail": "Une erreur est survenu lors du paiement",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
    payment_data = response.json()
    payment_url = payment_data.get("data", {}).get("payment_url")
    if not payment_url:
        error = {
            "detail": "Erreur CinetPay",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
    return error, {"payment_url": payment_url}


def cinetpaty_notify(
    *, cpm_trans_id: int, cpm_site_id: int
) -> tuple[dict[str, Union[str, int]]]:
    error_response, success_response = None, None
    if not cpm_trans_id or not cpm_site_id:
        error_response = {
            "detail": "Paramètres manquants",
            "status": status.HTTP_400_BAD_REQUEST,
        }

    try:
        order = Order.objects.get(id=cpm_trans_id)
    except Order.DoesNotExist:
        error_response = {
            "detail": "Commande introuvable",
            "status": status.HTTP_404_NOT_FOUND,
        }
    if order.status == Order.Status.PAID:
        success_response = {
            "detail": "Déjà traité",
            "status": status.HTTP_200_OK,
        }
    check_data = {
        "apikey": settings.CINETPAY_API_KEY,
        "site_id": settings.CINETPAY_SITE_ID,
        "transaction_id": str(cpm_trans_id),
    }
    check_response = requests.post(
        "https://api-checkout.cinetpay.com/v2/payment/check", json=check_data
    )
    if check_response.status_code != 200:
        error_response = {
            "detail": "Erreur vérification CinetPay",
            "status": status.HTTP_502_BAD_GATEWAY,
        }
    check_result = check_response.json()
    payment_status = check_result.get("data", {}).get("status")

    if payment_status == "ACCEPTED":
        order.status = Order.Status.PAID
        order.save()
    elif payment_status == "REFUSED":
        order.status = Order.Status.CANCELLED
        order.save()

    success_response = {"detail": "OK", "status": status.HTTP_200_OK}
    return error_response, success_response
