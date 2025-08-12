from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, permissions
from rest_framework.parsers import FormParser, MultiPartParser

from .models import Event
from .serializers import (
    EventDetailSerializer,
    EventListSerializer,
    EventWriteSerializer,
)


@extend_schema(
    summary="이벤트 목록 조회",
    parameters=[
        OpenApiParameter(name="page", description="페이지 번호", required=False, type=int),
        OpenApiParameter(name="only_active", description="진행 중인 필터(true/False)", required=False, type=bool),
    ],
)
class EventListView(generics.ListAPIView):
    serializer_class = EventListSerializer

    def get_queryset(self):
        qs = Event.objects.filter(is_active=True).order_by("id")
        only_active = self.request.GET.get("only_active")
        if str(only_active).lower() == "true":
            today = timezone.localdate()
            qs = qs.filter(start_date__lte=today, end_date__gte=today)
        return qs


extend_schema(summary="이벤트 상세 조회")


class EventDetailView(generics.RetrieveAPIView):
    serializer_class = EventDetailSerializer
    lookup_url_kwarg = "event_id"


class IsAdmin(permissions.IsAdminUser):
    pass


@extend_schema(summary="이벤트 등록(어드민)")
class AdminEventCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = EventWriteSerializer
    parser_classes = (MultiPartParser, FormParser)


@extend_schema(summary="이벤트 수정(어드민)")
class AdminEventUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Event.objects.all()
    serializer_class = EventWriteSerializer
    lookup_url_kwarg = "event_id"


@extend_schema(summary="이벤트 삭제(어드민)")
class AdminEventDeleteView(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Event.objects.all()
    lookup_url_kwarg = "event_id"
