from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.accounts'
    label = 'accounts'
    verbose_name = 'Аккаунты'
    