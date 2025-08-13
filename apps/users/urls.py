from django.urls import path

from apps.users.views.auth import LoginView, LogoutView, SignupView
from apps.users.views.social_login import KakaoLoginView

urlpatterns = [
    path("kakao/login/", KakaoLoginView.as_view(), name="kakao-login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
