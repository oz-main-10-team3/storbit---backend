from rest_framework import serializers

from apps.studies.models import StudyMember


class StudyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMember
        fields = [
            "id",
            "user",
            "level",
        ]
        read_only_fields = fields
