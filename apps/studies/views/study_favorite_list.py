from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.studies.models import StudyFavorite
from apps.studies.serializers.study_favorite_list import MyStudyFavoriteListSerializer


class MyStudyListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["스터디 찜"],
        summary="내가 찜한 스터디 목록 조회",
    )
    def get(self, request):
        qs = (
            StudyFavorite.objects.filter(user=request.user, is_active=True)
            .select_related("study")
            .order_by("-updated_at")
        )

        data = MyStudyFavoriteListSerializer(qs, many=True, context={"request": request}).data
        return Response(data, status=status.HTTP_200_OK)
