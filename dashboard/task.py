from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def send_otp_email(email, otp, expires_at_str):
    try:
        send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is: {otp}. It will expire at {expires_at_str}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )
    except Exception as e:
        logger.error(f"Error occurred while sending email for project task assignment. Error msg: {e}")
        return False
    else:
        logger.info(f"Email send successfully sent")
        return True