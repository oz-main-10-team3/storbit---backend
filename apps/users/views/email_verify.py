from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers.email_verify import (
    EmailVerificationSerializer,
    SendEmailSerializer,
)
from apps.users.tasks import send_password_email_task, send_signup_email_task
from apps.users.utils.base62 import generate_base62_code


class SignupSendEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SendEmailSerializer

    @extend_schema(tags=["이메일 인증"], summary="회원가입 이메일 인증")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        code = generate_base62_code(6)
        cache.set(email, code, timeout=300)

        send_signup_email_task.delay(email, code)
        return Response({"message": "회원가입 인증코드가 이메일로 전송되었습니다."}, status=status.HTTP_200_OK)


class EmailVerifyView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailVerificationSerializer

    @extend_schema(tags=["이메일 인증"], summary="이메일 인증코드 검증")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        cache_key = email
        cache_code = cache.get(cache_key)
        if not cache_code:
            return Response({"error": "인증코드가 만료되었거나 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if code != cache_code:
            return Response({"error": "인증코드가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(cache_key)
        cache.set(f"email_verified:{email}", code, timeout=300)
        return Response({"message": "이메일 인증이 완료되었습니다."}, status=status.HTTP_200_OK)


class PasswordSendEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SendEmailSerializer

    @extend_schema(tags=["이메일 인증"], summary="비밀번호 이메일 인증")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        code = generate_base62_code(6)
        cache_key = f"password_find_{email}"
        cache.set(cache_key, code, timeout=300)

        send_password_email_task.delay(email, code)
        return Response({"message": "회원가입 인증코드가 이메일로 전송되었습니다."}, status=status.HTTP_200_OK)


class PasswordEmailVerifyView:
    permission_classes = [AllowAny]
    serializer_class = EmailVerificationSerializer
