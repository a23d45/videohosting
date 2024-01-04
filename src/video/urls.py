from django.urls import path, include

from src.video import views


urlpatterns = [
    path('videos/', views.VideoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('videos/<int:pk>/', views.VideoViewSet.as_view(
        {
            'get': 'retrieve', 
            'put': 'update', 
            'patch': 'partial_update'
        }
    )),
    path(
        'videos/<int:pk>/watch/', 
        views.VideoViewSet.as_view({'get': 'watch'}),
        name='video_watch',
    ),
    path(
        'videos/<int:pk>/videoplayer/', 
        views.VideoViewSet.as_view({'get': 'videoplayer'}),
        name='video_html',
    ),
    path(
        'comments/',
        views.CommentAuthorView.as_view({'get': 'list', 'post': 'create'})
    ),
    path(
        'comments/<int:pk>/',
        views.CommentAuthorView.as_view({'get': 'retrieve', 'put': 'update'}),
    ),
    path('ratings/', views.RatingView.as_view()),
    path('genres/', views.GenreViewSet.as_view({'get': 'list'})),
    path('genres/<int:pk>/', views.GenreViewSet.as_view({'get': 'retrieve'})),
    path(
        'comments-by-video/<int:video_id>/', 
        views.CommentsOnVideoView.as_view()
    ),
    path('profile/watched/', views.WatchedVideoForUserView.as_view()),
    path('profile/my-videos/', views.VideosCreatedByUserView.as_view()),
    path('author/<int:pk>/videos/', views.AuthorVideosView.as_view()),
]