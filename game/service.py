import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_email_to_player(email_data: dict[str, Any]) -> None:
    try:
        send_mail(
            subject=email_data.get("subject"),
            message=email_data.get("message"),
            from_email=email_data.get("from_email"),
            recipient_list=email_data.get("recipient_list"),
            fail_silently=False,
        )
    except TimeoutError:
        msg = "Timeout error occur while sending euro million message, try later"
        logging.exception(msg)
    except Exception as exc:
        logging.exception(
            "Error occur while trying to send email million message %s", exc
        )


def bulk_send_email(**kwargs) -> None:
    subject = "Recapitulatif Jeu Euro Millions Monde"
    message_to_client = (
        "Numéros choisis de 1 à 50 "
        + kwargs.get("numbers")
        + "\n"
        + "Numeros choisis de 1 à 12"
        + kwargs.get("stars")
    )
    admin_message = f"M/Mme {kwargs.get('name')}{kwargs.get('surname')} avez choisi  \n {message_to_client}"
    email_tasks = [
        {
            "subject": subject,
            "message": message_to_client,
            "from_email": kwargs.get("from_email"),
            "recipient_list": [settings.EMAIL_EURO_MILLION_MONDE],
        },
        {
            "subject": subject,
            "message": admin_message,
            "from_email": settings.EMAIL_EURO_MILLION_MONDE,
            "recipient_list": [kwargs.get("from_email")],
        },
    ]
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(send_email_to_player, email_tasks)
