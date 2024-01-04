from django.apps import AppConfig


class VideoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.video'
    label = 'video'
    verbose_name = 'Видео'
    
