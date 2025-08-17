from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.validators import validate_email
from rest_framework import serializers

from apps.users.models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["fullname", "email", "nickname", "password", "phone_number", "gender"]
        extra_kwargs = {"password": {"write_only": True}, "email": {"validators": []}}

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("이미 가입된 이메일입니다.")

        verified = cache.get(f"email_verified:{email}")
        if not verified:
            raise serializers.ValidationError("이메일 인증이 완료되지 않았습니다.")

        cache.delete(verified)
        return email

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data, password=password)
        return user


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


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname", "phone_number", "profile_image"]

    def validate(self, attrs):
        user = self.instance

        if "nickname" in attrs:
            if User.objects.exclude(id=user.id).filter(nickname=attrs["nickname"]).exists():
                raise serializers.ValidationError({"nickname": "이미 사용 중인 닉네임입니다."})

        if "phone_number" in attrs:
            if User.objects.exclude(id=user.id).filter(phone_number=attrs["phone_number"]).exists():
                raise serializers.ValidationError({"phone_number": "이미 사용 중인 전화번호입니다."})

        return attrs
