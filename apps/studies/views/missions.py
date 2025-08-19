from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.studies.models import Study
from apps.studies.serializers.missions import LeaderMissionSerializer


class LeaderMissionCreateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LeaderMissionSerializer

    @extend_schema(tags=["미션"], summary="최종목표, 공통목표")
    def post(self, request, study_id):
        study = get_object_or_404(Study, id=study_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        mission = serializer.save(study=study)

        # WebSocket으로 브로드캐스트
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"study_{mission.study_id}",
            {
                "type": "mission_created",
                "mission": LeaderMissionSerializer(mission).data,
            },
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
