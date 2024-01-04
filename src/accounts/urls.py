from django.urls import path, re_path, include

from rest_framework_simplejwt import views


urlpatterns = [
    path('', include('src.accounts.auth_routes')),    
    re_path(r"^jwt/create/?", 
            views.TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^jwt/refresh/?", 
            views.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^jwt/verify/?", 
            views.TokenVerifyView.as_view(), name="jwt-verify"),
    re_path(r"^jwt/logout/?", 
            views.TokenBlacklistView.as_view(), name="jwt-blacklist"),
]
