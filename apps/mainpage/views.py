from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Study
from .serializers import MainStudySerializer


@extend_schema(
    summary="메인 스터디 리스트 조회",
    description="hot / new / steady 기준으로 정렬된 스터디 목록 반환 (최대 10개)",
    parameters=[
        OpenApiParameter(
            name="type", type=str, description="정렬 기준: hot(인기순), new(최신순), steady(출석률 높은 순)"
        ),
    ],
)
class MainStudyListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = MainStudySerializer

    def get_queryset(self):
        sort_type = self.request.query_params.get("type", "new")

        # 즐겨찾기 수 기준 필드 추가
        queryset = Study.objects.annotate(favorite_count=Count("favorited_by"))

        if sort_type == "hot":
            # HOT: 즐겨찾기 수 많은 순 + 최신순 → 10개 제한
            return queryset.order_by("-favorite_count", "-created_at")[:10]

        elif sort_type == "steady":
            # STEADY: 생성된 지 1주일 이상 + 즐겨찾기 많은 순 → 10개 제한
            one_week_ago = timezone.now() - timedelta(days=7)
            return queryset.filter(created_at__lte=one_week_ago).order_by("-favorite_count")[:10]

            # TODO: 출석률 기준 정렬이 명확해지면 아래처럼 수정 예정
            # return queryset.annotate(attendance_rate=...).order_by("-attendance_rate")[:10]

        # 기본은 NEW: 최신순 → 10개 제한
        return queryset.order_by("-created_at")[:10]
