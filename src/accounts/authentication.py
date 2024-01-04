from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

class EmailOrUsernameAuthBackend(ModelBackend):
    """Аутентификация по email или по username"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None