from django.utils import timezone
from rest_framework import serializers

from apps.events.models import Event


# 목록/조회용
class EventListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    is_progressing = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ("id", "title", "thumbnail_url", "is_active", "start_date", "end_date", "is_progressing")

    def get_thumbnail_url(self, obj):
        # event_image가 문자열이면 그대로 반환
        return obj.event_image or None

    def get_is_progressing(self, obj):
        today = timezone.localdate()
        return obj.is_active and obj.start_date <= today <= obj.end_date


# 상세조회용 (옵션)
class EventDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ("id", "title", "is_active", "start_date", "end_date", "image_url")

    def get_image_url(self, obj):
        return obj.event_image or None


# 등록/수정용
class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "event_image", "title", "is_active", "start_date", "end_date")

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and start > end:
            raise serializers.ValidationError("시작일은 마감일보다 이후일 수 없습니다.")
        return attrs
