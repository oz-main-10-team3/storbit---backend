from django.urls import path

from apps.users.views.auth import (
    LoginView,
    LogoutView,
    SignupView,
    UserDeleteView,
    UserDetailView,
    UserUpdateView,
)
from apps.users.views.email_verify import (
    EmailVerifyView,
    PasswordSendEmailView,
    SignupSendEmailView,
)
from apps.users.views.social_login import KakaoLoginView

urlpatterns = [
    path("kakao/login/", KakaoLoginView.as_view(), name="kakao-login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("send-code/", SignupSendEmailView.as_view(), name="signup-email-code"),
    path("code-verify/", EmailVerifyView.as_view(), name="email-verify"),
    path("password/send-code/", PasswordSendEmailView.as_view(), name="password-send-email"),
    path("profile/", UserDetailView.as_view(), name="user-detail"),
    path("profile/update/", UserUpdateView.as_view(), name="user-update"),
    path("profile/delete/", UserDeleteView.as_view(), name="user-delete"),
]
