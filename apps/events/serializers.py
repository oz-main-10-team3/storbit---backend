from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.events.models import Event, EventImage


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ("id", "event_image")


class EventListSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(source="event_image", many=True, read_only=True)  # 저장된 이미지 조회용

    class Meta:
        model = Event
        fields = ("id", "title", "images", "event_type", "event_status", "is_active", "start_date", "end_date")


class EventDetailSerializer(serializers.ModelSerializer):
    images = EventImageSerializer(source="event_image", many=True, read_only=True)  # 저장된 이미지 조회용

    class Meta:
        model = Event
        fields = ("id", "title", "images", "event_type", "event_status", "is_active", "start_date", "end_date")


# 등록/수정용
class EventCreateSerializer(serializers.ModelSerializer):
    event_image = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)
    images = EventImageSerializer(source="event_image", many=True, read_only=True)  # 저장된 이미지 조회용

    class Meta:
        model = Event
        fields = (
            "id",
            "event_image",
            "images",
            "title",
            "is_active",
            "start_date",
            "end_date",
            "event_status",
            "event_type",
        )

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and start > end:
            raise serializers.ValidationError("시작일은 마감일보다 이후일 수 없습니다.")
        return attrs

    def create(self, validated_data):
        images = validated_data.pop("event_image", [])  # 'event_image' 필드에서 이미지 리스트 꺼냄
        event = super().create(validated_data)
        for image in images:
            EventImage.objects.create(event=event, event_image=image)
        event.refresh_from_db()
        return event

    def update(self, instance, validated_data):
        images = validated_data.pop("event_image", [])
        instance = super().update(instance, validated_data)
        existing_images = instance.event_image.all()
        existing_images_dict = {img.event_image.name.split("/")[-1]: img for img in existing_images}

        for image in images:
            image_name = image.name
            if image_name in existing_images_dict:
                existing_img = existing_images_dict[image_name]
                existing_img.event_image = image
                existing_img.save()
                del existing_images_dict[image_name]
            else:
                EventImage.objects.create(event=instance, event_image=image)

        return instance
