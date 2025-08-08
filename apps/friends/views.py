from datetime import datetime

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FriendRequest
from .serializers import FriendRequestCreateSerializer, FriendRequestResponseSerializer


class FriendRequestCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=FriendRequestCreateSerializer,
        responses={201: FriendRequestCreateSerializer, 400: None},
        tags=["friends"],
        summary="친구 요청 보내기",
    )
    def post(self, request: Request) -> Response:
        serializer = FriendRequestCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FriendRequestRespondAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=FriendRequestResponseSerializer,
        responses={200: None, 404: None},
        tags=["friends"],
        summary="친구 요청 수락 또는 거절",
    )
    def post(self, request: Request, request_id: int) -> Response:
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user, status="pending")
        except FriendRequest.DoesNotExist:
            return Response({"detail": "친구 요청을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FriendRequestResponseSerializer(data=request.data, context={"friend_request": friend_request})
        serializer.is_valid(raise_exception=True)
        serializer.save(responded_at=datetime.now())

        return Response({"message": f"친구 요청이 {friend_request.status}되었습니다."})
