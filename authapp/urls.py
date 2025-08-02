from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authapp.views.logout_view import LogoutAPIView
from authapp.views.register_view import RegisterAPIView
from authapp.views.login_view import LoginAPIView
urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]