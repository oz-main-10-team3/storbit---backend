from rest_framework import serializers

from .models import Application


class StudyApplicationSerializer(serializers.ModelSerializer):
    """
    스터디 신청을 위한 시리얼라이저
    """

    class Meta:
        model = Application
        fields = ["nickname", "stack", "level", "motivation"]

    def validate_stack(self, value):
        # 기술 스택은 하나 이상 선택해야 함을 검사합니다.
        if not value:
            raise serializers.ValidationError("기술 스택은 하나 이상 선택해야 합니다.")
        return value

    def create(self, validated_data):
        # 중복 신청 방지 로직을 처리합니다.
        study_instance = validated_data.pop("study")
        if Application.objects.filter(study=study_instance, nickname=validated_data["nickname"]).exists():
            raise serializers.ValidationError("이미 해당 스터디에 신청했습니다.")

        return Application.objects.create(study=study_instance, **validated_data)
