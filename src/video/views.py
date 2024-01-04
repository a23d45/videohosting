import os

from django.http import FileResponse, Http404
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from src.services import db
from src.services.mediafiles import get_videofile_for_watch
from src.services.permissions import IsAuthor
from src.video import serializers
from src.video.models import Genre, Video, Comment
from src.video.pagination import VideoPagination


class VideoViewSet(viewsets.ModelViewSet):
    """Набор представлений для модели Video"""
    pagination_class = VideoPagination
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['title', 'genres']
    search_fields = ['title', 'author__username']
    ordering_fields = ['publication_date', 'views_count', 'likes']
    ordering = '-publication_date'

    def get_queryset(self):
        return db.get_public_or_is_author_video(user_id=self.request.user.id)

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'watch', 'videoplayer'):
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'): 
            return serializers.VideoSerializer
        return serializers.CreateOrUpdateVideoSerializer
    
    @action(detail=True, methods=['get'])
    def watch(self, request, pk=None):
        self.video_object = self.get_object()

        if os.path.exists(self.video_object.videofile.path):
            videofile, status_code, content_length, content_range =\
                get_videofile_for_watch(request, self.video_object)
            
            response =  FileResponse(
                videofile,
                filename=self.video_object.videofile.name,
                status=status_code,
                content_type='video/mp4'
            )
            response['Accept-Ranges'] = 'bytes'
            response['Content-Length'] = str(content_length)
            response['Cache-Control'] = 'no-cache'
            response['Content-Range'] = content_range
            return response
        return Http404

    @action(detail=True, methods=['get'])
    def videoplayer(self, request, pk=None):
        self.video_object = self.get_object()
        if self.video_object:

            db.set_views_count_on_video(
                video_obj=self.video_object,
                user=self.request.user
            )   
            return render(
                request=request, 
                template_name='video/videoplayer.html', 
                context={'video_object': self.video_object}
            )
        return Http404
        

class RatingView(generics.CreateAPIView):
    """Пользователь оценивает видео"""
    serializer_class = serializers.RatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        video_id = request.data.get('video_id')
        rating = request.data.get('rating')
        try:
            db.set_rating_for_video(
                video_id=video_id, 
                user=request.user, 
                rating=rating
            )
        except ValueError:
            raise PermissionDenied('Пользователь не посмотрел видео')
        return Response(status=200, data={'success': True})


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение жанров, доступных на платформе"""
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class CommentAuthorView(viewsets.ModelViewSet):
    """Получение комментариев, которые оставил текущий пользователь"""
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'): 
            return serializers.UpdateCommentSerializer
        return serializers.CommentSerializer


class CommentsOnVideoView(generics.ListAPIView):
    """Получение комментариев к видео"""
    lookup_field = 'video_id'
    serializer_class = serializers.CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.filter(
            video_id=self.kwargs.get(self.lookup_field)
        )


class WatchedVideoForUserView(generics.ListAPIView):
    """Пользователь получает список видео, которые он посмотрел"""
    serializer_class = serializers.VideoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = VideoPagination

    def get_queryset(self):
        return db.get_watched_videos_for_user(user_id=self.request.user.id)


class VideosCreatedByUserView(generics.ListAPIView):
    """Пользователь получает список видео, которые он создал"""
    serializer_class = serializers.VideoSerializer
    pagination_class = VideoPagination
    permission_classes = [IsAuthor]
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['title', 'genres', 'draft']
    search_fields = ['title']
    ordering_fields = ['publication_date', 'views_count', 'likes', 'dislikes', 'draft']
    ordering = ['-publication_date', '-draft']

    def get_queryset(self):
        return db.get_videos_created_by_user(self.request.user.id, True)


class AuthorVideosView(VideosCreatedByUserView):
    """
    Получение списка видео, которые создал пользователь.
    Отображаются те видео, у которых draft=False.
    """
    permission_classes = [AllowAny]
    filterset_fields = ['title', 'genres']
    search_fields = ['title']
    ordering_fields = ['publication_date', 'views_count', 'likes', 'dislikes']
    ordering = ['-publication_date']

    def get_queryset(self):
        return db.get_videos_created_by_user(
            self.kwargs.get(self.lookup_field), 
            False
        )
