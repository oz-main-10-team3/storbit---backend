from django.urls import path

from apps.users.views.auth import LoginView, LogoutView, SignupView
from apps.users.views.social_login import KakaoLoginView

urlpatterns = [
    path("kakao/login/", KakaoLoginView.as_view(), name="kakao-login"),
]
