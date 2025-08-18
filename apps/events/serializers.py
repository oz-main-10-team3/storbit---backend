from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.events.models import Event


# 목록/조회용
class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "title", "event_image", "is_active", "start_date", "end_date")


# 상세조회용 (옵션)
class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "title", "is_active", "start_date", "end_date", "event_image")


# 등록/수정용
class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "event_image", "title", "is_active", "start_date", "end_date")

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and start > end:
            raise serializers.ValidationError("시작일은 마감일보다 이후일 수 없습니다.")
        return attrs

    @extend_schema_field(OpenApiTypes.BINARY)
    def get_event_image(self, obj):
        return obj.event_image.url
