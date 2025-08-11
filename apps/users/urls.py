from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "users"

urlpatterns = [
    # 메인 페이지
    path("", TemplateView.as_view(template_name="users/home.html"), name="home"),
    # 인증 관련 URL
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.user_logout, name="logout"),
    # 카카오 로그인 관련 URL
    path("login/kakao/", views.KakaoLoginView.as_view(), name="kakao_login"),
    path("login/kakao/callback/", views.KakaoCallbackView.as_view(), name="kakao_callback"),
    # 사용자 프로필 관련 URL
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("profile/edit/", views.UserProfileEditView.as_view(), name="profile_edit"),
    # 회원 탈퇴 관련 URL
    path("withdrawal/", views.WithdrawalView.as_view(), name="withdrawal"),
    # API 엔드포인트 - 중복 확인
    path("api/check-email/", views.check_email_duplicate, name="check_email_duplicate"),
    path("api/check-nickname/", views.check_nickname_duplicate, name="check_nickname_duplicate"),
    # API 엔드포인트 - 관리자용 통계
    path("api/stats/", views.user_stats, name="user_stats"),
]
