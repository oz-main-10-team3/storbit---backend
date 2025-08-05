# apps/studies/serializers/study_serializers.py

from rest_framework import serializers

from apps.studies.models import Study


class StudyDetailSerializer(serializers.ModelSerializer):
    leader_id = serializers.IntegerField(source="leader.id")
    category_id = serializers.IntegerField(source="category.id")

    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "description",
            "thumbnail_url",
            "type",
            "member",
            "max_wait_member",
            "schedule",
            "level",
            "gender",
            "is_live",
            "is_active",
            "status",
            "leader_id",
            "category_id",
            "start_time",
            "end_time",
            "created_at",
            "updated_at",
        ]
