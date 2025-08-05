from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ValidationError
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # 일반 사용자 생성
        if not email:
            raise ValueError("이메일은 필수입니다.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        # 슈퍼유저 생성
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("슈퍼유저는 is_staff=True여야 합니다.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("슈퍼유저는 is_superuser=True여야 합니다.")

        return self.create_user(email, password, **extra_fields)

    def create_kakao_user(self, email, fullname, nickname, kakao_id, **extra_fields):
        # 카카오 로그인 사용자 생성
        user = self.create_user(
            email=email,
            fullname=fullname,
            nickname=nickname,
            password=None,  # 카카오 사용자는 비밀번호 없음
            **extra_fields,
        )

        # 카카오 소셜 계정 생성
        SocialAccount.objects.create(
            user=user,
            provider="KAKAO",
            provider_id=kakao_id,
            profile_image=extra_fields.get("profile_image", ""),
        )

        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ("M", "남성"),
        ("F", "여성"),
        ("O", "기타"),
    ]

    # 기본 정보
    fullname = models.CharField("성명", max_length=100)
    email = models.EmailField("이메일", unique=True)
    nickname = models.CharField("닉네임", max_length=50, unique=True)
    phone_number = models.CharField("전화번호", max_length=20, blank=True)

    # 프로필 정보
    gender = models.CharField("성별", max_length=1, choices=GENDER_CHOICES, blank=True)
    profile_image = models.URLField("프로필 이미지", blank=True)
    goal = models.TextField("목표", blank=True)

    # Django 인증 관련 필드
    is_active = models.BooleanField("활성 상태", default=True)
    is_staff = models.BooleanField("스태프 권한", default=False)

    # 타임스탬프
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname", "nickname"]

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자들"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["nickname"]),
        ]

    def __str__(self):
        return f"{self.fullname} ({self.email})"

    def get_full_name(self):
        return self.fullname

    def get_short_name(self):
        return self.nickname or self.fullname

    @property
    def is_kakao_user(self):
        # 카카오 로그인 사용자인지 확인
        return self.social_accounts.filter(provider="KAKAO").exists()

    @property
    def kakao_account(self):
        # 카카오 소셜 계정 반환
        return self.social_accounts.filter(provider="KAKAO").first()


class SocialAccount(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="social_accounts",
        verbose_name="사용자",
    )
    provider = models.CharField(
        "제공자", max_length=20, default="KAKAO"
    )  # 카카오만 사용
    provider_id = models.CharField("카카오 ID", max_length=255, unique=True)
    profile_image = models.URLField("프로필 이미지", blank=True)

    created_at = models.DateTimeField("생성일", auto_now_add=True)

    class Meta:
        db_table = "social_accounts"
        verbose_name = "카카오 계정"
        verbose_name_plural = "카카오 계정들"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["provider_id"]),
        ]

    def __str__(self):
        return f"{self.user.fullname} - 카카오"

    def clean(self):
        # 카카오만 허용하도록 검증
        if self.provider != "KAKAO":
            raise ValidationError("카카오 로그인만 지원됩니다.")

    def save(self, *args, **kwargs):
        self.provider = "KAKAO"  # 강제로 카카오 설정
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def get_user_by_kakao_id(cls, kakao_id):
        # 카카오 ID로 사용자 조회"""
        try:
            social_account = cls.objects.get(provider_id=kakao_id)
            return social_account.user
        except cls.DoesNotExist:
            return None


class Withdrawal(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="withdrawals",
        verbose_name="사용자",
    )
    reason = models.CharField("탈퇴 사유", max_length=255)
    description = models.TextField("상세 설명", blank=True)
    password = models.CharField("확인 비밀번호", max_length=255)  # 탈퇴 확인용

    created_at = models.DateTimeField("탈퇴 신청일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        db_table = "withdrawal"
        verbose_name = "회원 탈퇴"
        verbose_name_plural = "회원 탈퇴들"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return (
            f"{self.user.fullname} 탈퇴 신청 ({self.created_at.strftime('%Y-%m-%d')})"
        )

    def save(self, *args, **kwargs):
        # 탈퇴 신청시 사용자 비활성화
        super().save(*args, **kwargs)
        # 탈퇴 신청시 사용자를 비활성화
        if self.user.is_active:
            self.user.is_active = False
            self.user.save(update_fields=["is_active"])


# 사용자 관련 헬퍼 함수들
class UserService:
    @staticmethod
    def get_or_create_kakao_user(kakao_id, user_data):
        # 카카오 로그인 사용자 조회 또는 생성
        # 기존 카카오 계정으로 사용자 찾기
        user = SocialAccount.get_user_by_kakao_id(kakao_id)

        if user:
            return user, False  # 기존 사용자

        # 닉네임 중복 체크 및 자동 생성
        nickname = user_data.get("nickname", "")
        if not nickname or User.objects.filter(nickname=nickname).exists():
            base_nickname = user_data.get("fullname", "user")
            counter = 1
            while User.objects.filter(nickname=f"{base_nickname}{counter}").exists():
                counter += 1
            nickname = f"{base_nickname}{counter}"

        # 새 카카오 사용자 생성
        user = User.objects.create_kakao_user(
            email=user_data.get("email", ""),
            fullname=user_data.get("fullname", ""),
            nickname=nickname,
            kakao_id=kakao_id,
            profile_image=user_data.get("profile_image", ""),
            gender=user_data.get("gender", ""),
            phone_number=user_data.get("phone_number", ""),
        )

        return user, True  # 새 사용자

    @staticmethod
    def withdraw_user(user, reason, description="", password=""):
        # 사용자 탈퇴 처리
        return Withdrawal.objects.create(
            user=user, reason=reason, description=description, password=password
        )

    @staticmethod
    def get_kakao_profile_image(user):
        # 사용자의 카카오 프로필 이미지 반환
        kakao_account = user.kakao_account
        if kakao_account and kakao_account.profile_image:
            return kakao_account.profile_image
        return user.profile_image
