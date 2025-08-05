# apps/studies/views/study_views.py

from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.studies.models import Study
from apps.studies.serializers.study_serializers import StudyDetailSerializer


class StudyDetailView(APIView):
    @extend_schema(
        responses={200: StudyDetailSerializer},
        summary="스터디룸 상세 조회",
        tags=["스터디룸"],
    )
    def get(self, request, id: int, *args: Any, **kwargs: Any) -> Response:
        try:
            study = Study.objects.get(id=id)
        except Study.DoesNotExist:
            return Response({"detail": "스터디룸을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudyDetailSerializer(study)
        return Response(serializer.data, status=status.HTTP_200_OK)
