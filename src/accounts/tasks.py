from django.contrib.auth import get_user_model
from django.conf import settings
from djoser.email import PasswordResetEmail, UsernameResetEmail, ActivationEmail

from config.celery import app


User = get_user_model()

@app.task(bind=True, default_retry_delay=5 * 60)
def send_reset_password_email(self, context, to):
    try:
        user = User.objects.get(id=context['user_id'])
        context={'user': user}
        PasswordResetEmail(context=context).send(to)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

@app.task(bind=True, default_retry_delay=5 * 60)
def send_reset_username_email(self, context, to):
    try:
        user = User.objects.get(id=context['user_id'])
        context={'user': user}
        UsernameResetEmail(context=context).send(to)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

@app.task(bind=True, default_retry_delay=5 * 60)
def send_activation_email(self, context, to):
    try:
        user = User.objects.get(id=context['user_id'])
        context={'user': user}
        ActivationEmail(context=context).send(to)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)