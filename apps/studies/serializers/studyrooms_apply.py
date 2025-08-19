from rest_framework import serializers

from apps.studies.models import StudyMember


class StudyApplySerializer(serializers.Serializer):

    level = serializers.ChoiceField(
        choices=StudyMember._meta.get_field("level").choices, required=False, allow_null=True
    )

    description = serializers.CharField(required=True, allow_blank=False, help_text="자기소개")

    def create(self, validated_data):
        validated_data["is_permitted"] = False
        return StudyMember.objects.create(**validated_data)

    def validate(self, attrs):
        request = self.context.get("request")
        study = self.context.get("study")

        if StudyMember.objects.filter(study=study, user=request.user).exists():
            raise serializers.ValidationError("이미 신청했거나 멤버입니다.")
        return attrs
