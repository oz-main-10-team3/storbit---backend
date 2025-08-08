from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.studies.models import StudyApplication


class StudyApplicationSerializer(serializers.ModelSerializer):
    """
    스터디 신청을 위한 시리얼라이저.
    study와 user 필드의 조합이 고유한지 검증합니다.
    """

    class Meta:
        model = StudyApplication
        fields = ["id", "study", "user"]
        read_only_fields = ["user"]

        validators = [
            UniqueTogetherValidator(
                queryset=StudyApplication.objects.all(),  # type: ignore
                fields=["study", "user"],
                message="이미 해당 스터디에 신청했습니다.",
            )
        ]