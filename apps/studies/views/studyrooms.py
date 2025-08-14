from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.studies.models import Study, StudyMember
from apps.studies.serializers.studyrooms import (
    StudyCreateSerializer,
    StudySerializer,
    TransferLeaderSerializer,
)

User = get_user_model()


class IsStudyMaster(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            member = StudyMember.objects.get(study=obj, user=request.user)
            return member.role == StudyMember.MASTER
        except StudyMember.DoesNotExist:
            return False


@extend_schema(tags=["스터디"])
class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsStudyMaster]

    def get_serializer_class(self):
        if self.action == "create":
            return StudyCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        study = serializer.save()
        StudyMember.objects.create(study=study, user=self.request.user, role=StudyMember.MASTER, is_permitted=True)

    @extend_schema(summary="스터디 목록 조회", description="전체 스터디 목록을 최신순으로 조회합니다.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="스터디 상세 조회", description="특정 스터디의 상세 정보를 조회합니다.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="스터디 생성", description="새로운 스터디를 생성합니다. 생성하는 사용자가 방장이 됩니다.")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="스터디 수정", description="방장만 스터디 정보를 수정할 수 있습니다.")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="스터디 부분 수정", description="방장만 스터디 정보를 부분 수정할 수 있습니다.")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="스터디 삭제", description="방장만 스터디를 삭제할 수 있습니다.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="스터디 방장 권한 위임",
        description="현재 방장이 다른 스터디 멤버에게 방장 권한을 위임합니다.",
        request=TransferLeaderSerializer,
        responses={
            200: {"description": "방장 권한이 성공적으로 위임되었습니다."},
            400: {"description": "잘못된 요청"},
            403: {"description": "권한 없음"},
            404: {"description": "스터디 또는 멤버를 찾을 수 없음"},
        },
    )
    @action(detail=True, methods=["post"])
    def change_leader(self, request, pk=None):
        study = self.get_object()
        serializer = TransferLeaderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_leader_id = serializer.validated_data["user_id"]
        current_user = request.user

        try:
            current_leader = StudyMember.objects.get(study=study, user=current_user, role=StudyMember.MASTER)
        except StudyMember.DoesNotExist:
            return Response({"detail": "현재 방장만 권한을 변경할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        try:
            new_leader_member = StudyMember.objects.get(study=study, user_id=new_leader_id)
        except StudyMember.DoesNotExist:
            return Response({"detail": "지정한 사용자는 스터디 멤버가 아닙니다."}, status=status.HTTP_404_NOT_FOUND)

        if current_user.id == new_leader_id:
            return Response(
                {"detail": "자기 자신에게는 권한을 위임할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        current_leader.role = StudyMember.MEMBER
        current_leader.save()

        new_leader_member.role = StudyMember.MASTER
        new_leader_member.save()

        return Response(
            {"detail": f"방장이 {new_leader_member.user.username}님으로 변경되었습니다."}, status=status.HTTP_200_OK
        )
