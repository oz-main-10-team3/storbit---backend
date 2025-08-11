from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html

from .models import SocialAccount, User, Withdrawal


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """사용자 관리"""

    # 목록 화면 설정
    list_display = (
        "email",
        "fullname",
        "nickname",
        "gender",
        "is_active",
        "is_staff",
        "is_kakao_user_display",
        "created_at",
        "profile_image_display",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "gender", "created_at", "updated_at")
    search_fields = ("email", "fullname", "nickname", "phone_number")
    ordering = ("-created_at",)
    list_per_page = 25

    # 상세 화면 설정
    fieldsets = (
        ("기본 정보", {"fields": ("email", "fullname", "nickname")}),
        ("개인 정보", {"fields": ("phone_number", "gender", "profile_image", "goal")}),
        (
            "권한",
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
                "classes": ("collapse",),
            },
        ),
        ("중요한 일정", {"fields": ("last_login", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    # 새 사용자 생성 폼
    add_fieldsets = (
        (
            "기본 정보",
            {
                "classes": ("wide",),
                "fields": ("email", "fullname", "nickname", "password1", "password2"),
            },
        ),
        (
            "개인 정보",
            {
                "classes": ("wide",),
                "fields": ("phone_number", "gender", "profile_image", "goal"),
            },
        ),
        (
            "권한",
            {
                "classes": ("wide",),
                "fields": ("is_active", "is_staff"),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at", "last_login")
    filter_horizontal = ("groups", "user_permissions")

    @admin.display(description="로그인 타입", ordering="social_accounts")
    def is_kakao_user_display(self, obj):
        """카카오 사용자 여부 표시"""
        if obj.is_kakao_user:
            return format_html('<span style="color: #FEE500; font-weight: bold;">카카오</span>')
        return format_html('<span style="color: #666;">일반</span>')

    @admin.display(description="프로필 이미지")
    def profile_image_display(self, obj):
        """프로필 이미지 미리보기"""
        if obj.profile_image:
            return format_html('<img src="{}" width="30" height="30" style="border-radius: 50%;" />', obj.profile_image)
        return "-"

    def get_queryset(self, request):
        """쿼리셋 최적화"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("social_accounts")


class SocialAccountInline(admin.TabularInline):
    """사용자 상세 페이지에서 카카오 계정 인라인 편집"""

    model = SocialAccount
    extra = 0
    readonly_fields = ("provider", "provider_id", "created_at", "profile_image_preview")
    fields = ("provider", "provider_id", "profile_image", "profile_image_preview", "created_at")

    @admin.display(description="이미지 미리보기")
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%;" />', obj.profile_image)
        return "-"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    """카카오 계정 관리"""

    list_display = ("user_link", "provider", "provider_id", "profile_image_display", "created_at")
    list_filter = ("provider", "created_at")
    search_fields = ("user__email", "user__fullname", "provider_id")
    readonly_fields = ("provider", "created_at", "profile_image_display")
    ordering = ("-created_at",)

    fields = ("user", "provider", "provider_id", "profile_image", "profile_image_display", "created_at")

    @admin.display(description="사용자", ordering="user__fullname")
    def user_link(self, obj):
        """사용자 링크"""
        url = reverse("admin:users_user_change", args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.fullname)

    @admin.display(description="프로필 이미지")
    def profile_image_display(self, obj):
        """프로필 이미지 미리보기"""
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_image)
        return "-"

    def has_add_permission(self, request):
        """카카오 계정은 직접 생성 불가"""
        return False


class WithdrawalInline(admin.TabularInline):
    """사용자 상세 페이지에서 탈퇴 기록 인라인 표시"""

    model = Withdrawal
    extra = 0
    readonly_fields = ("reason", "description", "created_at", "updated_at")
    fields = ("reason", "description", "created_at", "updated_at")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    """회원 탈퇴 관리"""

    list_display = ("user_link", "reason", "description_short", "created_at", "user_status")
    list_filter = ("reason", "created_at", "user__is_active")
    search_fields = ("user__email", "user__fullname", "reason", "description")
    readonly_fields = ("user", "reason", "description", "password", "created_at", "updated_at")
    ordering = ("-created_at",)

    fields = ("user", "reason", "description", "password", "created_at", "updated_at")

    @admin.display(description="탈퇴 사용자", ordering="user__fullname")
    def user_link(self, obj):
        """사용자 링크"""
        url = reverse("admin:users_user_change", args=[obj.user.pk])
        return format_html('<a href="{}">{} ({})</a>', url, obj.user.fullname, obj.user.email)

    @admin.display(description="상세 설명")
    def description_short(self, obj):
        """상세 설명 요약"""
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "-"

    @admin.display(description="계정 상태", ordering="user__is_active")
    def user_status(self, obj):
        """사용자 상태"""
        if obj.user.is_active:
            return format_html('<span style="color: #28a745;">활성</span>')
        return format_html('<span style="color: #dc3545;">비활성</span>')

    def has_add_permission(self, request):
        """탈퇴 기록은 직접 생성 불가"""
        return False

    def has_change_permission(self, request, obj=None):
        """탈퇴 기록은 수정 불가"""
        return False


# UserAdmin에 인라인 추가
UserAdmin.inlines = [SocialAccountInline, WithdrawalInline]

# Admin 사이트 커스터마이징
admin.site.site_header = "사용자 관리 시스템"
admin.site.site_title = "관리자"
admin.site.index_title = "사용자 관리"
