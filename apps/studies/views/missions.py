from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.studies.models import Study
from apps.studies.serializers.missions import (
    DailyMissionSerializer,
    LeaderMissionSerializer,
)
from apps.users.models import User


class LeaderMissionCreateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LeaderMissionSerializer

    @extend_schema(tags=["미션"], summary="최종목표, 공통목표 생성")
    def post(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        mission = serializer.save(study=study)
        rsp_serializer = LeaderMissionSerializer(mission).data
        return Response(rsp_serializer, status=status.HTTP_201_CREATED)


class LeaderMissionDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LeaderMissionSerializer

    @extend_schema(tags=["미션"], summary="최종목표, 공통목표 상세 조회")
    def get(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)  # 스터디 조회
        leader_mission = study.leader_missions.first()  # 리드 미션 참조
        if not leader_mission:
            return Response({"detail": "리드 미션이 존재하지 않습니다."}, status=404)
        serializer = self.serializer_class(leader_mission)  # 직렬화
        return Response(serializer.data)


class DailyMissionDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DailyMissionSerializer

    def get(self, request, study_id):
        user = get_object_or_404(User, id=request.user.id)
        study = get_object_or_404(Study, id=study_id)
        pass


class DailyMissionCreateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DailyMissionSerializer

    @extend_schema(tags=["미션"], summary="데일리 미션 생성")
    def post(self, request, study_id):
        pass
