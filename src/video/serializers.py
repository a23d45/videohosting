from rest_framework import serializers

from src.video.models import Video, Genre, VideoRating, Comment
from src.services.db import (
    get_likes_count_on_video,
    get_dislikes_count_on_video, 
    check_user_watched_the_video,
    set_rating_for_video,
)
from src.services.mediafiles import delete_file


class GetUserFromRequestMixix:
    """Возвращает пользователя из контекста сериализатора"""
    def get_user(self):
        return self.context.get('request').user


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre"""
    class Meta:
        model = Genre
        fields = '__all__'


class CreateOrUpdateVideoSerializer(serializers.ModelSerializer):
    """Сериализатор модели Video для обновления или создания"""
    author = serializers.SlugRelatedField(
        slug_field='username', 
        read_only=True,
    )
    views_count = serializers.IntegerField(read_only=True)
    publication_date = serializers.DateTimeField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    draft = serializers.BooleanField(default=True)
    
    class Meta:
        model = Video
        fields = '__all__'

    def update(self, instance, validated_data):
        delete_file(instance.preview.path)
        delete_file(instance.videofile.path)
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        kwargs.setdefault('user', self.context.get('request').user)
        return super().save(**kwargs)
    

class VideoSerializer(CreateOrUpdateVideoSerializer):
    """Сериализатор видео для чтения"""
    genres = GenreSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField(method_name='get_likes')
    dislikes = serializers.SerializerMethodField(method_name='get_dislikes')

    def get_likes(self, obj: Video) -> int:
        return get_likes_count_on_video(obj)
    
    def get_dislikes(self, obj: Video) -> int:
        return get_dislikes_count_on_video(obj)


class RatingSerializer(serializers.Serializer):
    """Сериализатор для оценок"""
    video_id = serializers.IntegerField(required=True)
    rating = serializers.BooleanField(required=True)
    

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    user_id = serializers.IntegerField(read_only=True)
    video_id = serializers.IntegerField(required=True)

    class Meta:
        model = Comment
        fields = ('id', 'user_id', 'video_id', 'content')

    def validate(self, attrs):
        video_id = attrs.get('video_id')
        user_id = self.context.get('request').user.id
        if check_user_watched_the_video(video_id, user_id):
            return attrs
        raise serializers.ValidationError('Пользователь не смотрел видео')


class UpdateCommentSerializer(CommentSerializer):
    """
    Сериализатор, используемый для обновления комментария.
    Запрещено изменять video_id комментария.
    """
    video_id = serializers.IntegerField(read_only=True)