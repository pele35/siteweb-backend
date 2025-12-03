import logging
import random
from datetime import timezone
from typing import Dict
from typing import Union

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from ekila.send_mail import send_email
from tarifs.models import Order

logger = logging.getLogger(__name__)


def send_verification_code(*, user: User, order_id: int) -> None:
    order = get_object_or_404(Order, id=order_id, user=user)
    code = f"{random.randint(settings.MIN_NUMBER, settings.MAX_NUMBER)}"
    order.verification_code = code
    order.code_verified = False
    order.save()
    try:
        send_email(
            from_email=settings.FROM_EMAIL,
            to=user.email,
            subject="Code de confirmation de commande",
            message=f"""
                Bonjour {user.username},
                Votre code de confirmation pour la commande #{str(order.id)[0:6]} est : {code}.
                Veuillez entrer ce code pour vérifier votre email.
            """,
        )
    except Exception as exc:
        logging.exception("Error occur while trying to send email %s", exc)


def verify_code(
    user: User, order_id: int, code: int
) -> Dict[str, Union[bool, str, int]]:
    order = get_object_or_404(Order, id=order_id, user=user)
    if order.code_created_at:
        if (order.code_created_at + settings.DURATION_TIME_CODE) < timezone.now():
            return {"success": False, "detail": "Code expiré.", "status": 400}

    if order.verification_code == code:
        order.code_verified = True
        order.status = Order.Status.EMAIL_VERIFIED
        order.save()
        return {"success": True, "detail": "Code vérifié.", "status": 200}
    return {"success": False, "detail": "Code incorrect.", "status": 400}
