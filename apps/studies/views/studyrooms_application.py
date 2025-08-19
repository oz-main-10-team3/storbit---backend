from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.studies.models import StudyMember


class StudyMemberAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["스터디룸"],
        summary="스터디 참여 요청 수락",
    )
    @transaction.atomic
    def post(self, request, study_id: int, user_id: int):
        # 1) 방장 권한 확인
        is_master = StudyMember.objects.filter(
            study_id=study_id, user=request.user, role=StudyMember.Role.MASTER
        ).exists()
        if not is_master:
            return Response(
                {"message": "방장만 수락할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        member = get_object_or_404(StudyMember, study_id=study_id, user=user_id)
        if member is None:
            return Response(
                {"message": "해당 사용자가 스터디에 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
        member.is_permitted = True
        member.save(update_fields=["is_permitted"])

        return Response(
            {
                "message": "참여 요청을 수락했습니다.",
                "member_id": member.id,
                "study_id": member.study_id,
                "user_id": member.user_id,
                "is_permitted": member.is_permitted,
            },
            status=status.HTTP_200_OK,
        )
