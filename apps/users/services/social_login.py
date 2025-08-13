import requests

from apps.users.models import UserService
from config.settings.base import (
    KAKAO_APP_CLIENT,
    KAKAO_CLIENT_SECRET,
    KAKAO_REDIRECT_URI,
)


class KakaoLoginService:
    @staticmethod
    def get_access_token(code: str) -> str:
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": KAKAO_APP_CLIENT,
            "client_secret": KAKAO_CLIENT_SECRET,
            "redirect_uri": KAKAO_REDIRECT_URI,
            "code": code,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=data, headers=headers)
        if response.status_code != 200:
            raise Exception(f"토큰 요청 실패: {response.status_code}")
        return response.json()

    @staticmethod
    def get_user_info(access_token: str):
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        response = requests.post(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"카카오 사용자 정보 요청 실패: {response.text}")

        return response.json()

    @staticmethod
    def create_kakao_user(access_token: str):
        user_info = KakaoLoginService.get_user_info(access_token)

        # 3. 유저 정보 추출
        kakao_id = user_info.get("id")
        kakao_account = user_info.get("kakao_account", {})
        kakao_profile = kakao_account.get("profile", {})
        profile_image = kakao_profile.get("profile_image_url", "")
        email = kakao_account.get("email")
        nickname = kakao_profile.get("nickname")

        user, created = UserService.get_or_create_kakao_user(
            kakao_id=kakao_id,
            user_data={
                "email": email,
                "fullname": nickname,
                "nickname": nickname,
                "profile_image": profile_image,
            },
        )
        return user, True
