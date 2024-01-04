from django.urls import path
from django.contrib.auth import get_user_model
from src.accounts.views import CustomUserViewSet as UserViewSet


User = get_user_model() 

profile_detail = UserViewSet.as_view({
    'get': 'me',
    'patch': 'me',
    'put': 'me',
    'delete': 'me',
})

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'})),
    path('profile/', profile_detail),
    path('activation/', 
         UserViewSet.as_view({'post': 'activation'})),
    path('resend_activation/', 
         UserViewSet.as_view({'post': 'resend_activation'})), # повторная отправка email с подтверждением регистрации
    path(f'set_{User.USERNAME_FIELD}/', 
         UserViewSet.as_view({'post': 'set_username'})), # изменить имя пользователя
    path(f'reset_{User.USERNAME_FIELD}/', 
         UserViewSet.as_view({'post': 'reset_username'})), # отправка email для сброса имени usera, авторизация не нужна
    path(f'reset_{User.USERNAME_FIELD}_confirm/', 
         UserViewSet.as_view({'post': 'reset_username_confirm'})), # отправка post запроса с фронтенда для сброса имени
    path('set_password/', 
         UserViewSet.as_view({'post': 'set_password'})), # изменить пароль пользователя
    path('reset_password/', 
         UserViewSet.as_view({'post': 'reset_password'})), # отправка email для смены пароля, авторизация не нужна
    path('reset_password_confirm/', 
         UserViewSet.as_view({'post': 'reset_password_confirm'})),# отправка post запроса с фронтенда для сброса пароля
]
