import os
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode

from apps.account.models import User
from config.celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task()
def send_mail_reset_password(user_id, *args, **kwargs):
    user = User.objects.get(id=user_id)
    uidb64 = urlsafe_base64_encode(smart_bytes(user_id))
    token = PasswordResetTokenGenerator().make_token(user)
    current_site = os.getenv('current_site')
    protocol = os.getenv('protocol')
    a = f'{uidb64}/{token}/'
    abs_url = f"{protocol}://{current_site}/account/api/user/password-token/" + a
    subject = 'Hi! Episode'
    message = f'Reset Password link:\n\n{abs_url}'
    send_mail(subject=subject,
              message=message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[user.email],
              fail_silently=True
              )
    return f"Send email successfully"

