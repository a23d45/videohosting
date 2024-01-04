from rest_framework.permissions import IsAuthenticated

class IsAuthor(IsAuthenticated):
    """Дает разрешение только автору видео"""
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'author'):
            return request.user == obj.author
        return request.user == obj.user


# class IsWatchedVideo(IsAuthenticated):

#     def has_permission(self, request, view):
#         request.user == 
#         super().has_permission(request, view)
#         #  bool(request.user and request.user.is_authenticated)