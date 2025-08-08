from django.db.models import Count
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.studies.models import Study
from apps.studies.serializers.mainpage_serializer import MainStudySerializer


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
        limit = int(self.request.query_params.get("limit", 10))
        offset = int(self.request.query_params.get("offset", 0))
        category_id = self.request.query_params.get("category_id", None)

        # 즐겨찾기 수 기준 필드 추가
        queryset = Study.objects.annotate(favorite_count=Count("favorited_by"))

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if sort_type == "hot":
            queryset = queryset.order_by("-favorite_count", "-created_at")
        elif sort_type == "steady":
            queryset = queryset.order_by("-created_at")

        else:
            queryset = queryset.order_by("-created_at")

        return queryset[offset : offset + limit]
