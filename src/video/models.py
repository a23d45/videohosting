from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone

from src.accounts.models import User
from src.services.mediafiles import (
    get_path_upload_preview, 
    get_path_upload_videofile,
    validate_video_size,
)


class Genre(models.Model):
    """Модель жанра"""
    name = models.CharField(
        verbose_name='Название',
        max_length=30,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f"Genre: {self.id} {self.name}"


class Video(models.Model):
    """Модель видео"""
    title = models.CharField(
        verbose_name='Название',
        max_length=50,
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    preview = models.ImageField(
        verbose_name='Превью',
        upload_to=get_path_upload_preview,
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
        ],
    )
    videofile = models.FileField(
        verbose_name='Видео',
        upload_to=get_path_upload_videofile,
        validators=[
            FileExtensionValidator(['mp4']),
            validate_video_size,
        ],
    )
    views_count = models.PositiveIntegerField(
        verbose_name='Количество просмотров',
        default=0,
    )
    draft = models.BooleanField(
        verbose_name='Черновик',
        default=True,
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    publication_date = models.DateTimeField(
        verbose_name='Дата публикации',
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        on_delete=models.CASCADE,
        related_name='videos',
    )
    genres = models.ManyToManyField(
        verbose_name='Жанры',
        to=Genre,
        related_name='videos',
    )

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def save(self, *args, **kwargs):
        if not self.draft and self.publication_date is None:
            self.publication_date = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Video: {self.id} {self.title}"


class Comment(models.Model):
    """Модель комментария"""
    content = models.TextField(
        verbose_name='Содержание',
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    video = models.ForeignKey(
        verbose_name='Видео',
        to=Video,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Comment: {self.id}"


class VideoRating(models.Model):
    """Оценка видео пользователем: лайк или дизлайк"""
    RATINGS = (
        (False, 'Дизлайк'),
        (True, 'Лайк'),
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    video = models.ForeignKey(
        verbose_name='Видео',
        to=Video,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    rating = models.BooleanField(
        verbose_name='Оценка',
        choices=RATINGS,
    )

    class Meta:
        unique_together = ('user', 'video')
        verbose_name = 'Оценка видео'
        verbose_name_plural = 'Оценки видео'

    def __str__(self):
        return f"Rating: {self.id}"


class WatchedVideo(models.Model):
    """Модель просмотренного видео"""
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
    )
    video = models.ForeignKey(
        verbose_name='Видео',
        to=Video,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('user', 'video')
        verbose_name = 'Просмотренное видео'
        verbose_name_plural = 'Просмотренные видео'

    def __str__(self):
        return f"WatchedVideo: {self.id}"