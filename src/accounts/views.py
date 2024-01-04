from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import UserViewSet

from src.accounts import tasks


User = get_user_model()

class CustomUserViewSet(UserViewSet):
    
    def generate_context_for_send_email(self, user_id: int) -> dict:
        return {
            'user_id': user_id,
            'domain': self.request.get_host(),
            'protocol': 'https' if self.request.is_secure() else 'http',
            'site_name': self.request.get_host()
        }

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = self.generate_context_for_send_email(user.id)
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
             tasks.send_activation_email.delay(context, to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)

    def perform_update(self, serializer, *args, **kwargs):
        super().perform_update(serializer, *args, **kwargs)
        user = serializer.instance
        signals.user_updated.send(
            sender=self.__class__, user=user, request=self.request
        )

        # should we send activation email after update?
        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            context = self.generate_context_for_send_email(user.id)
            to = [get_user_email(user)]
            tasks.send_activation_email.delay(context, to)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()
        
        if user:
            context = self.generate_context_for_send_email(user.id)
            tasks.send_reset_password_email.delay(
                context,
                [get_user_email(user)]
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}")
    def reset_username(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = self.generate_context_for_send_email(user.id)
            tasks.send_reset_username_email.delay(
                context,
                [get_user_email(user)]
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(is_active=False)

        if not settings.SEND_ACTIVATION_EMAIL or not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        context = self.generate_context_for_send_email(user.id)
        tasks.send_activation_email.delay(
            context,
            [get_user_email(user)]
        )

        return Response(status=status.HTTP_204_NO_CONTENT)