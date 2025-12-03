import logging
import mimetypes
import os
import smtplib
import socket
from email.message import EmailMessage
from typing import List
from typing import Optional

from django.conf import settings

logger = logging.getLogger(__name__)


def send_email(
    *,
    from_email: str,
    to: str,
    subject: str,
    message: str = None,
    html_message: str = None,
    attachments: Optional[List[str]] = None,
):
    """
    Send email with optional HTML content and attachments
    This support only SSL connection

    Args:
        from_email: Sender email address
        to: Recipient email address(es) - can be string or list
        subject: Email subject
        message: Plain text message (optional if html_message provided)
        html_message: HTML formatted message (optional)
        attachments: List of file paths to attach (optional)
    """
    try:
        msg = EmailMessage()
        msg["From"] = from_email
        msg["To"] = to
        msg["Subject"] = subject

        if message and html_message:
            msg.set_content(message)
            msg.add_alternative(html_message, subtype="html")
        elif html_message:
            msg.set_content(html_message, subtype="html")
        elif message:
            msg.set_content(message)
        else:
            error_msg = "Either message or html_message must be provided"
            raise ValueError(error_msg)

        if attachments:
            for attachment_path in attachments:
                attachment_path = os.path.normpath(attachment_path)
                if not os.path.exists(attachment_path):
                    logger.warning(f"Attachment file not found: {attachment_path}")
                    continue

                filename = os.path.basename(attachment_path)
                try:
                    with open(attachment_path, "rb") as file:
                        file_data = file.read()

                    mime_type, _ = mimetypes.guess_type(attachment_path)
                    file_type = mime_type if mime_type else "application/octet-stream"
                    msg.add_attachment(
                        file_data,
                        maintype=file_type.split("/")[0]
                        if "/" in file_type
                        else "application",
                        subtype=file_type.split("/")[1]
                        if "/" in file_type
                        else "octet-stream",
                        filename=filename,
                    )
                except Exception as e:
                    logger.exception(
                        f"Failed to process attachment {attachment_path}: {e}"
                    )
                    continue

        server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=30)
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(msg)
        server.quit()
        return 1
    except (socket.timeout, smtplib.SMTPException) as exc:
        logger.exception(f"Email sending failed: {exc}")
        return 0
    except Exception as exc:
        logger.exception(f"Error occurred while sending email: {exc}")
        return 0
