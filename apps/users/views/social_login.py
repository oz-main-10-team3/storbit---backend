from django.http.response import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.users.serializers.kakao import KakaoLoginSerializer
from apps.users.services.social_login import KakaoLoginService


class KakaoLoginView(APIView):
    serializer_class = KakaoLoginSerializer

    @extend_schema(tags=["사용자"], summary="카카오소셜 로그인")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]
        if not code:
            return JsonResponse({"error": "인가 코드(code)가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # 1. 인가 코드로 Access / Refresh Token 발급
            token_data = KakaoLoginService.get_access_token(code)
            access_token = token_data.get("access_token")

            if not access_token:
                return JsonResponse({"error": "Access Token 발급 실패"}, status=status.HTTP_400_BAD_REQUEST)

            user, created = KakaoLoginService.create_kakao_user(access_token)

            access = AccessToken.for_user(user)
            refresh = RefreshToken.for_user(user)

            return JsonResponse(
                {
                    "access_token": str(access),
                    "refresh_token": str(refresh),
                    "kakao_id": user.kakao_account.provider_id,
                    "nickname": user.nickname,
                    "email": user.email,
                    "profile_image": user.profile_image,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
