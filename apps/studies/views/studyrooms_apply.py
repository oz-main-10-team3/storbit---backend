from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.studies.models import Study, StudyMember
from apps.studies.serializers.studyrooms_apply import StudyApplySerializer


class StudyApplyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["스터디"],
        summary="스터디 신청",
        description="특정 스터디에 참여 신청을 생성합니다.",
        request=StudyApplySerializer,
        responses={201: dict},
    )
    @transaction.atomic
    def post(self, request, study_id: int):
        study = get_object_or_404(Study, id=study_id)

        approved_count = StudyMember.objects.filter(study=study, is_permitted=True).count()
        pending_count = StudyMember.objects.filter(study=study, is_permitted=False).count()

        if approved_count >= study.member and pending_count >= study.max_wait_member:
            return Response({"detail": "정원 및 대기열이 가득 찼습니다."}, status=status.HTTP_409_CONFLICT)

        serializer = StudyApplySerializer(data=request.data, context={"request": request, "study": study})
        serializer.is_valid(raise_exception=True)

        level = serializer.validated_data.get("level") or StudyMember.Level.ANY

        member = StudyMember.objects.create(
            user=request.user,
            study=study,
            role=StudyMember.Role.MEMBER,
            level=level,
            is_permitted=False,
        )

        return Response(
            {
                "message": "신청이 완료되었습니다.",
                "member_id": member.id,
                "study_id": study.id,
                "is_permitted": member.is_permitted,
                "role": member.role,
                "level": member.level,
                "approved_count": approved_count,
                "pending_count": pending_count + 1,
            },
            status=status.HTTP_201_CREATED,
        )
