from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    '''Модель пользователя'''
    REQUIRED_FIELDS = [
        'id', 
        'email', 
        'gender',
        'country',
        'bio',
        'avatar',
    ]
    CHOICES = [
        ('M', 'Мужской'),
        ('W', 'Женский'),
        ('', 'Не указано'),
    ]
    gender = models.CharField(
        verbose_name='Пол',
        choices=CHOICES,
        max_length=1,
        default='',
        blank=True, 
    )
    country = models.CharField(
        verbose_name='Страна',
        max_length=60, 
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to='avatar/',
        blank=True,
        null=True,
    )
    bio = models.TextField(
        verbose_name='О себе',
        max_length=200,
        blank=True,
        null=True,
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. \
                Letters, digits and @/./+/-/_ only.'
        ),
        validators=[
            AbstractUser.username_validator,
            RegexValidator('^[^@]*$')  # строка любой длины, не содержащая @
        ],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(_('email address'), unique=True)

