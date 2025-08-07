from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.studies.models import StudyApplication
from apps.studies.serializers.application_serializers import StudyApplicationSerializer


@extend_schema(
    summary="스터디 신청",
    description="사용자가 특정 스터디에 신청합니다. 이미 신청했거나 스터디가 존재하지 않으면 오류를 반환합니다.",
    request=StudyApplicationSerializer,
    responses={
        201: {"description": "스터디 신청 성공", "response": StudyApplicationSerializer},
        400: {"description": "잘못된 요청 또는 이미 신청함"},
        401: {"description": "인증되지 않은 사용자"},
        404: {"description": "스터디를 찾을 수 없음"},
    },
)
class StudyApplicationCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudyApplicationSerializer
    queryset = StudyApplication.objects.all()  # type: ignore

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
