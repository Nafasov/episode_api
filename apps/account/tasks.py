from django.contrib.auth import get_user_model
from config.celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task()
def send_mail_reset_password(self, user, *args, **kwargs):
    subject = 'Hi! Episode'
    message = f'Reset Password'
    send_mail(subject=subject,
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[user.email],
              fail_silently=True
              )
    return f"Send mail successfully"

