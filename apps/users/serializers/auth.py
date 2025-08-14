from django.contrib.auth import authenticate
from django.core.validators import validate_email
from rest_framework import serializers

from apps.users.models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["fullname", "email", "nickname", "password", "phone_number", "gender"]
        extra_kwargs = {"password": {"write_only": True}}


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise serializers.ValidationError("이메일과 비밀번호를 모두 입력해주세요.")

        try:
            validate_email(email)
        except Exception:
            raise serializers.ValidationError("이메일 형식이 올바르지 않습니다.")

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.")

        if not user.is_active:
            raise serializers.ValidationError("비활성화된 계정입니다.")

        data["user"] = user
        return data
