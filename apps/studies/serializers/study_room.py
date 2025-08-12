from rest_framework import serializers

from apps.studies.models import StudyRoom


class StudyRoomSerializer(serializers.ModelSerializer):

    owner_username = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = StudyRoom
        fields = ["id", "owner", "owner_username", "title", "description", "max_members", "created_at"]
        read_only_fields = ["id", "owner", "owner_username", "created_at"]
