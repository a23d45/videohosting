from django.contrib import admin
from django.utils.safestring import mark_safe

from src.accounts.models import User
from src.services.mixins import SettingsForAdminMixin

admin.site.site_header = 'Видеохостинг'


@admin.register(User)
class UserAdmin(SettingsForAdminMixin, admin.ModelAdmin):
	list_display = ['username', 'email', 'display_avatar']
	search_fields = ['username', 'email']
	list_filter = ['is_staff', 'gender']

	@admin.display(description='Аватар')
	def display_avatar(self, object):
		if object.avatar:
			return mark_safe(f'<img src="{object.avatar.url}" width=50>')