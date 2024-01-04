from django.contrib import admin
from django.utils.safestring import mark_safe

from src.video.models import Genre, Video, Comment, VideoRating, WatchedVideo
from src.services.mixins import SettingsForAdminMixin


@admin.register(Genre)
class GenreAdmin(SettingsForAdminMixin, admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['name']


@admin.register(Video)
class VideoAdmin(SettingsForAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'author', 'display_preview']
    readonly_fields = ['views_count', 'created', 'author']
    search_fields = ['title']
    ordering = ['-created', 'title', 'views_count']
    list_filter = ['draft', 'genres']

    @admin.display(description='Превью видео')
    def display_preview(self, object):
        if object.preview:
            return mark_safe(f'<img src="{object.preview.url}" width=50>')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    

@admin.register(Comment)
class CommentAdmin(SettingsForAdminMixin, admin.ModelAdmin):
    list_display = ['video', 'user', 'created']
    readonly_fields = ['user', 'video']

    def has_add_permission(self, request):
        return False


@admin.register(VideoRating)
class VideoRatingAdmin(SettingsForAdminMixin, admin.ModelAdmin):
    list_display = ['video', 'user', 'rating']
    readonly_fields = ['user', 'video']
    search_fields = ['user__username', 'video__title']

    def has_add_permission(self, request):
        return False


@admin.register(WatchedVideo)
class WatchedVideoAdmin(SettingsForAdminMixin, admin.ModelAdmin):
    list_display = ['video', 'user']
    readonly_fields = ['user', 'video']
    search_fields = ['user__username', 'video__title']

    def has_add_permission(self, request):
        return False


