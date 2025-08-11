from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import SocialAccount, User, UserService, Withdrawal


class UserRegistrationSerializer(serializers.ModelSerializer):
    """사용자 회원가입"""

    password = serializers.CharField(write_only=True, style={"input_type": "password"}, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("email", "fullname", "nickname", "password", "password_confirm", "phone_number", "gender", "goal")

    def validate(self, attrs):
        """비밀번호 확인 검증"""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return attrs

    def validate_email(self, value):
        """이메일 중복 검증"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 존재하는 이메일입니다.")
        return value

    def validate_nickname(self, value):
        """닉네임 중복 검증"""
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 존재하는 닉네임입니다.")
        return value

    def create(self, validated_data):
        """사용자 생성"""
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """사용자 로그인"""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        """로그인 인증 검증"""
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("이메일 또는 비밀번호가 잘못되었습니다.")
            if not user.is_active:
                raise serializers.ValidationError("비활성화된 계정입니다. 관리자에게 문의하세요.")
            attrs["user"] = user
        else:
            raise serializers.ValidationError("이메일과 비밀번호를 입력해주세요.")

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필"""

    profile_image = serializers.SerializerMethodField()
    is_kakao_user = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullname",
            "nickname",
            "phone_number",
            "gender",
            "goal",
            "profile_image",
            "created_at",
            "updated_at",
            "is_active",
            "is_kakao_user",
        )
        read_only_fields = ("id", "email", "created_at", "updated_at", "is_active")

    def get_profile_image(self, obj):
        """카카오 프로필 이미지 또는 일반 프로필 이미지 URL 반환"""
        return UserService.get_kakao_profile_image(obj)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """사용자 프로필 수정"""

    class Meta:
        model = User
        fields = ("fullname", "nickname", "phone_number", "gender", "goal", "profile_image")

    def validate_nickname(self, value):
        """닉네임 중복 검증 (자신 제외)"""
        user = self.instance
        if User.objects.filter(nickname=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("이미 존재하는 닉네임입니다.")
        return value


class SocialAccountSerializer(serializers.ModelSerializer):
    """소셜 계정"""

    class Meta:
        model = SocialAccount
        fields = ("provider", "provider_id", "profile_image", "created_at")
        read_only_fields = ("provider", "created_at")


class KakaoUserDataSerializer(serializers.Serializer):
    """카카오 사용자 정보"""

    email = serializers.EmailField(required=False, allow_blank=True)
    fullname = serializers.CharField(required=False, allow_blank=True)
    nickname = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.URLField(required=False, allow_blank=True)
    gender = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)


class KakaoUserCreateSerializer(serializers.Serializer):
    """카카오 사용자 생성/조회"""

    kakao_id = serializers.CharField()
    user_data = KakaoUserDataSerializer()

    def create(self, validated_data):
        """카카오 사용자 생성 또는 조회"""
        kakao_id = validated_data["kakao_id"]
        user_data = validated_data["user_data"]

        user, created = UserService.get_or_create_kakao_user(kakao_id, user_data)
        return {"user": user, "created": created}


class WithdrawalSerializer(serializers.ModelSerializer):
    """회원 탈퇴"""

    password = serializers.CharField(write_only=True, required=False, style={"input_type": "password"})

    class Meta:
        model = Withdrawal
        fields = ("reason", "description", "password")

    def validate(self, attrs):
        """비밀번호 검증 (일반 사용자의 경우)"""
        user = self.context.get("user")

        # 카카오 사용자가 아닌 경우 비밀번호 필수
        if user and not user.is_kakao_user:
            password = attrs.get("password")
            if not password:
                raise serializers.ValidationError("비밀번호를 입력해주세요.")
            if not user.check_password(password):
                raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")

        return attrs

    def create(self, validated_data):
        """탈퇴 처리"""
        user = self.context.get("user")
        return UserService.withdraw_user(
            user=user,
            reason=validated_data["reason"],
            description=validated_data.get("description", ""),
            password=validated_data.get("password", ""),
        )


class WithdrawalDetailSerializer(serializers.ModelSerializer):
    """탈퇴 상세 정보"""

    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Withdrawal
        fields = ("id", "user", "reason", "description", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class EmailCheckSerializer(serializers.Serializer):
    """이메일 중복 확인"""

    email = serializers.EmailField()

    def validate_email(self, value):
        """이메일 형식 검증"""
        return value


class NicknameCheckSerializer(serializers.Serializer):
    """닉네임 중복 확인"""

    nickname = serializers.CharField(max_length=50)

    def validate_nickname(self, value):
        """닉네임 길이 검증"""
        if len(value) < 2:
            raise serializers.ValidationError("닉네임은 최소 2자 이상이어야 합니다.")
        return value


class UserStatsSerializer(serializers.Serializer):
    """사용자 통계"""

    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    kakao_users = serializers.IntegerField()
    regular_users = serializers.IntegerField()
    withdrawal_count = serializers.IntegerField()


class PasswordChangeSerializer(serializers.Serializer):
    """비밀번호 변경"""

    old_password = serializers.CharField(write_only=True, style={"input_type": "password"})
    new_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}, validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        """비밀번호 변경 검증"""
        user = self.context.get("user")

        # 카카오 사용자는 비밀번호 변경 불가
        if user and user.is_kakao_user:
            raise serializers.ValidationError("카카오 로그인 사용자는 비밀번호를 변경할 수 없습니다.")

        # 기존 비밀번호 확인
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError("기존 비밀번호가 일치하지 않습니다.")

        # 새 비밀번호 확인
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError("새 비밀번호가 일치하지 않습니다.")

        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    """사용자 상세 정보 (관리자용)"""

    social_accounts = SocialAccountSerializer(many=True, read_only=True)
    withdrawals = WithdrawalDetailSerializer(many=True, read_only=True)
    is_kakao_user = serializers.BooleanField(read_only=True)
    kakao_account = SocialAccountSerializer(read_only=True)
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullname",
            "nickname",
            "phone_number",
            "gender",
            "goal",
            "profile_image",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
            "updated_at",
            "last_login",
            "social_accounts",
            "withdrawals",
            "is_kakao_user",
            "kakao_account",
            "profile_image_url",
        )
        read_only_fields = ("id", "created_at", "updated_at", "last_login")

    def get_profile_image_url(self, obj):
        """프로필 이미지 URL 반환"""
        return UserService.get_kakao_profile_image(obj)


class UserListSerializer(serializers.ModelSerializer):
    """사용자 목록"""

    is_kakao_user = serializers.BooleanField(read_only=True)
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullname",
            "nickname",
            "is_active",
            "created_at",
            "is_kakao_user",
            "profile_image_url",
        )
        read_only_fields = ("id", "created_at")

    def get_profile_image_url(self, obj):
        """프로필 이미지 URL 반환"""
        return UserService.get_kakao_profile_image(obj)


class KakaoTokenSerializer(serializers.Serializer):
    """카카오 토큰 응답"""

    access_token = serializers.CharField()
    token_type = serializers.CharField()
    refresh_token = serializers.CharField(required=False)
    expires_in = serializers.IntegerField(required=False)
    scope = serializers.CharField(required=False)


class KakaoUserInfoSerializer(serializers.Serializer):
    """카카오 사용자 정보 응답"""

    id = serializers.CharField()
    connected_at = serializers.DateTimeField(required=False)
    properties = serializers.DictField(required=False)
    kakao_account = serializers.DictField(required=False)


class ErrorResponseSerializer(serializers.Serializer):
    """에러 응답"""

    error = serializers.CharField()
    detail = serializers.CharField(required=False)
    code = serializers.CharField(required=False)
    field_errors = serializers.DictField(required=False)


class SuccessResponseSerializer(serializers.Serializer):
    """성공 응답"""

    message = serializers.CharField()
    data = serializers.DictField(required=False)


class DuplicateCheckResponseSerializer(serializers.Serializer):
    """중복 확인 응답"""

    exists = serializers.BooleanField()
    message = serializers.CharField(required=False)


class LoginResponseSerializer(serializers.Serializer):
    """로그인 응답"""

    user = UserProfileSerializer()
    message = serializers.CharField()
    redirect_url = serializers.CharField(required=False)
