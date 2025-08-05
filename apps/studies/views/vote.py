from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from apps.studies.models import Vote
from apps.studies.serializers.vote import VoteSerializer

class VoteCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=VoteSerializer,
        responses={201: VoteSerializer},
        tags=["studies"],
        summary="스터디 투표 생성 API"
    )
    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)