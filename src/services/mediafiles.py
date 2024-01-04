import os
from typing import IO, Generator

from django.core.exceptions import ValidationError
from django.http import HttpResponse


GIGABYTES_VIDEO_LIMIT = 40

def get_path_upload_avatar(instance, filename):
    """
    Построение пути к аватарке пользователя,
    format: media/avatar/author_<id>/avatar.jpg
    """
    return f'avatar/user_{instance.id}/{filename}'


def get_path_upload_videofile(instance, filename):
    """
    Построение пути к видеофайлу,
    format: media/video/author_<id>/videofile.mp4
    """
    return f'video/video_{instance.author.id}/{filename}'


def get_path_upload_preview(instance, filename):
    """
    Построение пути к превью видео,
    format: media/preview/author_<id>/preview.jpg
    """
    return f'preview/preview_{instance.author.id}/{filename}'


def validate_video_size(file_obj):
    """Проверка размера видео"""
    if file_obj.size * 1024 ** 3 < GIGABYTES_VIDEO_LIMIT:
        raise ValidationError(
            f'Максимальный размер видео {GIGABYTES_VIDEO_LIMIT}ГБ'
        )


def delete_file(path_file):
    """Удаляет файл"""
    if os.path.exists(path_file):
        os.remove(path_file)


def get_video_response(file_obj):
    """Возвращает HttpResponse с видеофайлом, если он существует"""
    if os.path.exists(file_obj.path):
        pass


def get_byte_range(file: IO[bytes], 
           start: int, 
           end: int, 
           block_size: int=8192
           ) -> Generator[bytes, None, None]:
    """
    Возвращает объект-генератор, который возращает
    байты файла из заданного диапозона
    """
    consumed = 0

    file.seek(start)
    while True:
        if end:
            chunk = min(block_size, end - start - consumed)
        else:
            chunk = block_size
        if chunk <= 0:
            break
        data = file.read(chunk)
        if not data:
            break
        consumed += chunk
        yield data

    if hasattr(file, 'close'):
        file.close()



def get_videofile_for_watch(request: HttpResponse, video_obj) -> tuple:
    """
    Если задан http заголовок range, то возвращает байты 
    видео, которые находятся в заданном диапозоне 
    и http заголовки для ответа.
    Если заголовка range нет, то возвращается всё видео и 
    http заголовки для ответа.
    """
    file_size = video_obj.videofile.size

    videofile = open(video_obj.videofile.path, 'rb')
    status_code = 206
    content_length = file_size
    content_range = request.headers.get('range')

    if content_range is not None:
        content_range = content_range.strip().split('=')[-1] 
        start, end, *_ = map(str.strip, (content_range + '-').split('-'))
        start = int(start) if start else 0
        end = min(file_size - 1, int(end)) if end else file_size - 1
        content_length = (end - start) + 1
        print(start, end)
        videofile = get_byte_range(videofile, start, end + 1)
        status_code = 206
        content_range = f'bytes {start}-{end}/{file_size}'

    return videofile, status_code, content_length, content_range