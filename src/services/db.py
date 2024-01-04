from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.utils import IntegrityError
from django.db import connection


from src.video.models import VideoRating, WatchedVideo, Video, VideoRating


User = get_user_model()


def get_likes_count_on_video(video_obj: Video) -> int:
    """Возвращает количество лайков на видео"""
    return VideoRating.objects.filter(video=video_obj, rating=1).count()


def get_dislikes_count_on_video(video_obj: Video) -> int:
    """Возвращает количество дизлайков на видео"""
    return VideoRating.objects.filter(video=video_obj, rating=0).count()


def set_views_count_on_video(video_obj: Video, user: User) -> None:
    """
    Увеличивает количество просмотров на видео.
    Если пользователь авторизован, то создает экземпляр WatchedVideo
    и сохраняет его в БД.
    """
    if user.is_authenticated:
        WatchedVideo.objects.get_or_create(video=video_obj, user=user)
    video_obj.views_count += 1
    video_obj.save()


def check_user_watched_the_video(video_id: int, user_id: int) -> bool:
    """Проверяет, смотрел ли пользователь видео"""
    return WatchedVideo.objects.\
        filter(video_id=video_id, user_id=user_id).exists()


def set_rating_for_video(video_id: int, user_id: int, rating: bool) -> None:
    """
    Ставит оценку видео пользователем. 
    Если пользователь не смотрел видео, то вызывается исключение ValueError.
    """
    if check_user_watched_the_video(video_id, user_id):
        VideoRating.objects.update_or_create(
            user=user, 
            video_id=video_id, 
            defaults={'rating': rating}
        )
    else:
        raise ValueError

   
def get_public_or_is_author_video(user_id: int):
    """
    Возвращает экземпляры Video, у которых draft=False 
    или если user является автором
    """
    return Video.objects.filter(
        Q(draft=False) | Q(author__id=user_id)
    ).order_by('-publication_date')


def get_watched_videos_for_user(user_id: int):
    """Возвращает список видео, которые посмотрел пользователь"""
    list_with_video_ids = WatchedVideo.objects.filter(
        user_id=user_id
    ).values('video_id')
    return Video.objects.filter(id__in=list_with_video_ids)


def get_videos_created_by_user(user_id: int, with_draft:bool = False):
    """Возвращает список видео, которые создал пользователь"""
    if with_draft:
        return Video.objects.filter(author_id=user_id)
    return Video.objects.filter(author_id=user_id, draft=False)