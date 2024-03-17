import os
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from config.celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task()
def send_mail_reset_password(self, user, *args, **kwargs):
    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    current_site = os.getenv('current_site')
    protocol = os.getenv('protocol')
    abs_url = f'{protocol}://{current_site}/password/changed/{uidb64}/{token}'
    subject = 'Hi! Episode'
    message = f'Reset Password link:\n\n{abs_url}'
    send_mail(subject=subject,
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[user.email],
              fail_silently=True
              )
    return f"Send mail successfully"

