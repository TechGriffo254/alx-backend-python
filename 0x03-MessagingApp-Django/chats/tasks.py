from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_notification_email(self, subject, message, recipient_list):
    '''
    Send email notification asynchronously using Celery.
    
    Args:
        subject: Email subject
        message: Email body
        recipient_list: List of recipient email addresses
    '''
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(f'Email sent successfully to {recipient_list}')
        return f'Email sent to {len(recipient_list)} recipient(s)'
    except Exception as exc:
        logger.error(f'Failed to send email: {str(exc)}')
        raise self.retry(exc=exc, countdown=60)

@shared_task
def send_welcome_email(user_email, username):
    '''Send welcome email to new users'''
    subject = 'Welcome to MessagingApp!'
    message = f'Hello {username},\n\nWelcome to our messaging platform! We are excited to have you on board.'
    return send_notification_email(subject, message, [user_email])

@shared_task
def send_message_notification(recipient_email, sender_username, message_preview):
    '''Send notification when user receives a new message'''
    subject = f'New message from {sender_username}'
    message = f'You have a new message from {sender_username}:\n\n{message_preview}'
    return send_notification_email(subject, message, [recipient_email])
