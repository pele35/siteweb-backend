import base64
import json
import logging

from django.conf import settings
from django.core.mail import send_mail

from miscellaneous.models import Subscriber

logger = logging.getLogger(__name__)


def encode_subscriber_data(email: str, confirmation_code: str) -> str:
    data = {"email": email, "code": confirmation_code}
    json_data = json.dumps(data)
    encoded_data = base64.urlsafe_b64encode(json_data.encode()).decode()
    return encoded_data


def decode_subscriber_data(encoded_data: str) -> dict:
    try:
        decoded_data = base64.urlsafe_b64decode(encoded_data.encode()).decode()
        return json.loads(decoded_data)
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def send_subscriber_email(user: Subscriber) -> None:
    try:
        encoded_data = encode_subscriber_data(user.email, user.confirmation_code)
        confirmation_url = (
            f"{settings.FRONT_URI}/newsletter/confirm?data={encoded_data}"
        )

        html_message = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Confirmation Newsletter</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f8f9fa;
                    margin: 0;
                    padding: 20px;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: #ffffff;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                .email-header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px 20px;
                    text-align: center;
                }}
                .email-body {{
                    padding: 40px 30px;
                    color: #333333;
                }}
                .confirmation-code {{
                    background: #f8f9fa;
                    border: 2px dashed #dee2e6;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 20px 0;
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    color: #495057;
                }}
                .btn-confirm {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    padding: 12px 30px;
                    font-size: 16px;
                    border-radius: 25px;
                    color: white;
                    text-decoration: none;
                    display: inline-block;
                    margin: 20px 0;
                    transition: transform 0.2s;
                }}
                .btn-confirm:hover {{
                    transform: translateY(-2px);
                    color: white;
                    text-decoration: none;
                }}
                .email-footer {{
                    background: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #6c757d;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1> Bienvenue sur notre Newsletter !</h1>
                    <p>Confirmez votre adresse email pour recevoir nos actualités</p>
                </div>
                
                <div class="email-body">
                    <h2>Bonjour,</h2>
                    <p>Merci de vous être inscrit à notre newsletter. Pour finaliser votre inscription, veuillez confirmer votre adresse email.</p>
                    
                    <div class="confirmation-code">
                        Code de confirmation :<br>
                        <span style="color: #667eea; font-size: 24px;">{user.confirmation_code}</span>
                    </div>
                    
                    <p style="text-align: center;">
                        <a href="{confirmation_url}" class="btn-confirm">
                            Confirmer mon inscription
                        </a>
                    </p>
                    
                    <p>Si le bouton ne fonctionne pas, vous pouvez copier-coller ce lien dans votre navigateur :</p>
                    <p style="word-break: break-all; color: #667eea;">
                        <small>{confirmation_url}</small>
                    </p>
                    
                    <p style="color: #6c757d; font-size: 14px;">
                        Ce code expirera dans 24 heures pour des raisons de sécurité.
                    </p>
                </div>
                
                <div class="email-footer">
                    <p>© 2025 mnlv.com. Tous droits réservés.</p>
                    <p> 
                        <a href="{settings.FRONT_URI}/unsubscribe" style="color: #667eea; text-decoration: none;">
                            Se désabonner
                        </a>
                    </p>
                </div>
            </div>
        </body>
        </html>
    """

        send_mail(
            subject="Confirmation de votre inscription à la newsletter",
            message=f"""
                Bonjour,

                Merci de vous être inscrit à notre newsletter !

                Voici votre code de confirmation : {user.confirmation_code}

                Pour confirmer votre inscription, cliquez sur ce lien :
                {confirmation_url}

                Si le lien ne fonctionne pas, copiez-collez l'URL dans votre navigateur.

                Ce code expirera dans 24 heures.

                Cordialement,
                L'équipe mnlvm Media
            """,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info(f"Email de confirmation envoyé à {user.email}")

    except Exception as exc:
        logger.exception(
            "Erreur survenue lors de l'envoi du mail de confirmation à %s: %s",
            user.email,
            exc,
        )
        raise
