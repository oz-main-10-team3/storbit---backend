from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.models import User
from apps.users.serializers.auth import LoginSerializer, SignupSerializer


class SignupView(APIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["사용자"], summary="이메일 회원가입")
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)

        response = SignupSerializer(user)
        return Response(response.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(tags=["사용자"], summary="이메일 로그인")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "email": user.email,
                "nickname": user.nickname,
                "fullname": user.fullname,
                "profile_image": user.profile_image,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["사용자"], summary="사용자 로그아웃")
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "refresh 토큰이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트 DB에 저장

            return Response({"message": "로그아웃 완료"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "유효하지 않은 또는 만료된 토큰"}, status=status.HTTP_400_BAD_REQUEST)
