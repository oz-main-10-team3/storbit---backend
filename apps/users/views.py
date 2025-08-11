import logging

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from .forms import UserRegistrationForm, WithdrawalForm
from .models import SocialAccount, User, UserService, Withdrawal

logger = logging.getLogger(__name__)


class UserRegistrationView(View):
    """일반 회원가입"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("users:profile")
        form = UserRegistrationForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("users:profile")

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f"{user.fullname}님, 회원가입이 완료되었습니다.")
                return redirect("users:login")  # 성공 후 로그인 페이지로
            except IntegrityError:
                messages.error(request, "이미 존재하는 이메일 또는 닉네임입니다.")
            except Exception as e:
                logger.error(f"Registration error: {e}")
                messages.error(request, "회원가입 중 오류가 발생했습니다.")

        return render(request, "users/register.html", {"form": form})


class UserLoginView(View):
    """일반 로그인"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("users:profile")
        return render(request, "users/login.html")

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("users:profile")

        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "이메일과 비밀번호를 입력해주세요.")
            return render(request, "users/login.html")

        if user is not None:
            if user.is_active:
                login(request, user)
                # 로그인 성공 후 리디렉션할 페이지 설정 (예: 메인 페이지나 대시보드)
                next_url = request.GET.get("next", "/")  # 메인 페이지로 리디렉션
                messages.success(request, f"{user.fullname}님, 환영합니다!")
                return redirect(next_url)
            else:
                messages.error(request, "비활성화된 계정입니다. 관리자에게 문의하세요.")
        else:
            messages.error(request, "이메일 또는 비밀번호가 잘못되었습니다.")

        return render(request, "users/login.html")


class KakaoLoginView(View):
    """카카오 로그인"""

    def get(self, request):
        """카카오 로그인 페이지로 리디렉션"""
        kakao_auth_url = (
            f"https://kauth.kakao.com/oauth/authorize"
            f"?client_id={settings.KAKAO_CLIENT_ID}"
            f"&redirect_uri={settings.KAKAO_REDIRECT_URI}"
            f"&response_type=code"
        )
        return HttpResponseRedirect(kakao_auth_url)


class KakaoCallbackView(View):
    """카카오 로그인 콜백"""

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            messages.error(request, "카카오 로그인에 실패했습니다.")
            return redirect("users:login")

        try:
            # 액세스 토큰 요청
            token_data = self._get_kakao_token(code)
            if not token_data:
                messages.error(request, "카카오 토큰 획득에 실패했습니다.")
                return redirect("users:login")

            # 사용자 정보 요청
            user_data = self._get_kakao_user_info(token_data["access_token"])
            if not user_data:
                messages.error(request, "카카오 사용자 정보 획득에 실패했습니다.")
                return redirect("users:login")

            # 사용자 생성 또는 조회
            kakao_id = str(user_data["id"])
            user, created = UserService.get_or_create_kakao_user(
                kakao_id,
                {
                    "email": user_data.get("kakao_account", {}).get("email", ""),
                    "fullname": user_data.get("properties", {}).get("nickname", ""),
                    "nickname": user_data.get("properties", {}).get("nickname", ""),
                    "profile_image": user_data.get("properties", {}).get("profile_image", ""),
                    "gender": self._get_gender_from_kakao(user_data),
                },
            )

            if user.is_active:
                login(request, user)
                # 카카오 로그인 성공 후 리디렉션할 페이지 설정
                success_url = "/"  # 메인 페이지나 대시보드로 변경
                if created:
                    messages.success(request, f"{user.fullname}님, 카카오 회원가입이 완료되었습니다!")
                else:
                    messages.success(request, f"{user.fullname}님, 환영합니다!")
                return redirect(success_url)
            else:
                messages.error(request, "비활성화된 계정입니다.")
                return redirect("users:login")

        except Exception as e:
            logger.error(f"Kakao login error: {e}")
            messages.error(request, "카카오 로그인 중 오류가 발생했습니다.")
            return redirect("users:login")

    def _get_kakao_token(self, code):
        """카카오 액세스 토큰 획득"""
        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_CLIENT_ID,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "code": code,
        }

        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json()
        return None

    def _get_kakao_user_info(self, access_token):
        """카카오 사용자 정보 획득"""
        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(user_info_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def _get_gender_from_kakao(self, user_data):
        """카카오 데이터에서 성별 추출"""
        gender = user_data.get("kakao_account", {}).get("gender")
        if gender == "male":
            return "M"
        elif gender == "female":
            return "F"
        return ""


@method_decorator(login_required, name="dispatch")
class UserProfileView(View):
    """사용자 프로필"""

    def get(self, request):
        return render(
            request,
            "users/profile.html",
            {
                "user": request.user,
                "is_kakao_user": request.user.is_kakao_user,
                "profile_image": UserService.get_kakao_profile_image(request.user),
            },
        )


@method_decorator(login_required, name="dispatch")
class UserProfileEditView(View):
    """프로필 수정"""

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, "users/profile_edit.html", {"form": form})

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "프로필이 성공적으로 수정되었습니다.")
                return redirect("users:profile")
            except IntegrityError:
                messages.error(request, "이미 존재하는 닉네임입니다.")
            except Exception as e:
                logger.error(f"Profile update error: {e}")
                messages.error(request, "프로필 수정 중 오류가 발생했습니다.")

        return render(request, "users/profile_edit.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class WithdrawalView(View):
    """회원 탈퇴"""

    def get(self, request):
        form = WithdrawalForm()
        return render(request, "users/withdrawal.html", {"form": form, "is_kakao_user": request.user.is_kakao_user})

    def post(self, request):
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            # 카카오 사용자가 아닌 경우 비밀번호 확인
            if not request.user.is_kakao_user:
                password = form.cleaned_data.get("password")
                if not request.user.check_password(password):
                    messages.error(request, "비밀번호가 일치하지 않습니다.")
                    return render(request, "users/withdrawal.html", {"form": form})

            try:
                with transaction.atomic():
                    # 탈퇴 기록 생성
                    UserService.withdraw_user(
                        user=request.user,
                        reason=form.cleaned_data["reason"],
                        description=form.cleaned_data.get("description", ""),
                        password=form.cleaned_data.get("password", ""),
                    )

                    # 로그아웃
                    logout(request)
                    messages.success(request, "회원 탈퇴가 완료되었습니다.")
                    return redirect("users:home")

            except Exception as e:
                logger.error(f"Withdrawal error: {e}")
                messages.error(request, "탈퇴 처리 중 오류가 발생했습니다.")

        return render(request, "users/withdrawal.html", {"form": form, "is_kakao_user": request.user.is_kakao_user})


def user_logout(request):
    """로그아웃"""
    logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect("users:home")


# API Views
@require_http_methods(["GET"])
def check_email_duplicate(request):
    """이메일 중복 확인 API"""
    email = request.GET.get("email")
    if not email:
        return JsonResponse({"error": "이메일이 필요합니다."}, status=400)

    exists = User.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})


@require_http_methods(["GET"])
def check_nickname_duplicate(request):
    """닉네임 중복 확인 API"""
    nickname = request.GET.get("nickname")
    if not nickname:
        return JsonResponse({"error": "닉네임이 필요합니다."}, status=400)

    exists = User.objects.filter(nickname=nickname).exists()
    return JsonResponse({"exists": exists})


@login_required
@require_http_methods(["GET"])
def user_stats(request):
    """사용자 통계 API (관리자용)"""
    if not request.user.is_staff:
        return JsonResponse({"error": "권한이 없습니다."}, status=403)

    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    kakao_users = User.objects.filter(social_accounts__provider="KAKAO").count()
    withdrawal_count = Withdrawal.objects.count()

    return JsonResponse(
        {
            "total_users": total_users,
            "active_users": active_users,
            "kakao_users": kakao_users,
            "regular_users": total_users - kakao_users,
            "withdrawal_count": withdrawal_count,
        }
    )


# 에러 핸들링
def handler404(request, exception):
    """404 에러 핸들러"""
    return render(request, "users/404.html", status=404)


def handler500(request):
    """500 에러 핸들러"""
    return render(request, "users/500.html", status=500)
