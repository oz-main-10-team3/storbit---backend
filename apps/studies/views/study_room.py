from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.studies.models import Study, StudyMember
from apps.studies.serializers.study_room import (
    StudyRoomCreateSerializer,
    StudyRoomSerializer,
)

User = get_user_model()


class StudyRoomListAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StudyRoomCreateSerializer

    @extend_schema(
        tags=["스터디룸"],
        summary="스터디룸 목록 조회",
        description="전체 스터디룸 목록을 최신순으로 조회합니다.",
        responses=StudyRoomSerializer,
    )
    def get(self, request):
        qs = Study.objects.all().order_by("-id")
        data = self.serializer_class(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class StudyRoomCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=["스터디룸"],
        summary="스터디룸 생성",
        description="새로운 스터디룸을 생성합니다.",
        request=StudyRoomCreateSerializer,
        responses=StudyRoomSerializer,
    )
    def post(self, request):
        serializer = StudyRoomCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        study_room = serializer.save()

        StudyMember.objects.create(
            study_id=study_room.id,
            user=request.user,
            role=StudyMember.Role.MASTER,
            is_permitted=True,
        )
        return Response(StudyRoomSerializer(study_room).data, status=status.HTTP_201_CREATED)


class StudyRoomDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Study, pk=pk)

    @extend_schema(
        tags=["스터디룸"],
        summary="스터디룸 상세 조회",
        description="특정 스터디룸의 상세 정보를 조회합니다.",
        responses=StudyRoomSerializer,
    )
    def get(self, request, pk):
        obj = self.get_object(pk)
        return Response(StudyRoomSerializer(obj).data, status.HTTP_200_OK)

    @extend_schema(
        tags=["스터디룸"],
        summary="스터디룸 수정",
        description="방장만 스터디룸 정보를 수정할 수 있습니다.",
        request=StudyRoomSerializer,
        responses=StudyRoomSerializer,
    )
    def put(self, request, pk):
        obj = self.get_object(pk)
        self.check_object_permissions(request, obj)
        serializer = StudyRoomSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(StudyRoomSerializer(obj).data, status.HTTP_200_OK)

    @extend_schema(
        tags=["스터디룸"],
        summary="스터디룸 삭제",
        description="방장만 스터디룸을 삭제할 수 있습니다.",
        responses={204: None},
    )
    def delete(self, request, pk):
        obj = self.get_object(pk)
        self.check_object_permissions(request, obj)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
