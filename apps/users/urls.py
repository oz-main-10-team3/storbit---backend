from django.urls import path

from apps.users.views.auth import SignupView, LoginView, LogoutView
from apps.users.views.social_login import KakaoLoginView

urlpatterns = [
    path("kakao/login/", KakaoLoginView.as_view(), name="kakao-login"),
]
