from rest_framework import serializers

from apps.studies.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "study", "question", "created_at"]
        read_only_fields = ["id", "created_at"]
