from rest_framework import serializers

from apps.studies.models import Study, StudyFavorite


class StudyBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "thumbnail_url",
            "type",
            "member",
            "schedule",
            "level",
            "gender",
            "is_live",
            "status",
            "start_time",
            "end_time",
        ]


class MyStudyFavoriteListSerializer(serializers.ModelSerializer):
    study = StudyBriefSerializer(read_only=True)
    favorite_at = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = StudyFavorite
        fields = ["id", "study", "is_active", "favorite_at", "updated_at"]
        read_only_fields = ["id", "study", "is_active", "favorite_at", "updated_at"]
