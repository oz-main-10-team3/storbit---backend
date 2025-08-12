from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.studies.models import StudyRoom
from apps.studies.serializers.study_room import StudyRoomSerializer

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    방장(owner)만 수정/삭제, 권한 위임 가능
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


@extend_schema(tags=["스터디룸"])
class StudyRoomViewSet(viewsets.ModelViewSet):
    """
    스터디룸 CRUD 및 방장 위임 API
    """

    queryset = StudyRoom.objects.all()
    serializer_class = StudyRoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @extend_schema(summary="스터디룸 목록 조회", description="전체 스터디룸 목록을 최신순으로 조회합니다.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="스터디룸 상세 조회", description="특정 스터디룸의 상세 정보를 조회합니다.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="스터디룸 생성", description="새로운 스터디룸을 생성합니다. 생성하는 사용자가 방장이 됩니다."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="스터디룸 수정", description="방장만 스터디룸 정보를 수정할 수 있습니다.")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(summary="스터디룸 부분 수정", description="방장만 스터디룸 정보를 부분 수정할 수 있습니다.")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary="스터디룸 삭제", description="방장만 스터디룸을 삭제할 수 있습니다.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="스터디룸 방장 권한 위임",
        description="현재 방장이 다른 사용자에게 방장 권한을 위임합니다.",
        request=None,
        responses={200: None, 403: None, 404: None},
    )
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def change_owner(self, request, pk=None):
        study_room = self.get_object()
        if study_room.owner != request.user:
            return Response({"detail": "현재 방장만 권한을 변경할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        new_owner_id = request.data.get("new_owner_id")
        if not new_owner_id:
            return Response({"detail": "new_owner_id를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_owner = User.objects.get(id=new_owner_id)
        except User.DoesNotExist:
            return Response({"detail": "지정한 사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        study_room.owner = new_owner
        study_room.save()
        return Response({"detail": f"방장이 {new_owner.username}님으로 변경되었습니다."})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
