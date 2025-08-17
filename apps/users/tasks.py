from celery import shared_task

from apps.users.services.send_email import SendEmailService


@shared_task
def send_signup_email_task(email, code):
    SendEmailService.signup_send_email(email, code)


@shared_task
def send_password_email_task(email, code):
    SendEmailService.find_password_send_email(email, code)
