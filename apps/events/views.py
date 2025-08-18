import datetime

from django.db.models.functions import TruncDate
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event
from .serializers import (
    EventCreateSerializer,
    EventDetailSerializer,
    EventListSerializer,
)


class EventListView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EventListSerializer

    @extend_schema(tags=["이벤트"], summary="이벤트 목록조회")
    def get(self, request):
        qs = Event.objects.all()
        only_active = str(request.query_params.get("only_active", "")).lower()

        if only_active == "true":
            today = datetime.datetime.now().date()
            qs = qs.annotate(
                start_date=TruncDate("start_date"),
                end_date=TruncDate("end_date"),
            ).filter(start_date__lte=today, end_date__gte=today)

        serializer = self.serializer_class(qs, many=True, context={"request": request})
        return Response(serializer.data)


class EventDetailView(APIView):
    serializer_class = EventDetailSerializer
    permissions_classes = (permissions.AllowAny,)

    @extend_schema(tags=["이벤트"], summary="이벤트 상세조회")
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(event, context={"request": request})
        return Response(serializer.data)


class AdminEventCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = EventCreateSerializer

    @extend_schema(tags=["이벤트"], summary="이벤트 생성")
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminEventUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = EventCreateSerializer

    @extend_schema(tags=["이벤트"], summary="이벤트 수정")
    def put(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(event, data=request.data, partial=False, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminEventDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=["이벤트"], summary="이벤트 삭제")
    def delete(self, request, *args, **kwargs):
        event_id = kwargs.get("event_id")
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
