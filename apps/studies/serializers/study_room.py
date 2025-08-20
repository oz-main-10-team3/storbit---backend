from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.studies.models import Study, StudyMember

User = get_user_model()


class StudyRoomSerializer(serializers.ModelSerializer):
    leader_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "description",
            "thumbnail_url",
            "type",
            "member_count",
            "max_wait_member",
            "level",
            "gender",
            "is_live",
            "status",
            "leader_name",
            "category",
            "category_name",
            "schedule",
            "start_time",
            "end_time",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def get_leader_name(self, obj):
        try:
            leader_member = obj.studymember_set.get(role=StudyMember.Role.MASTER)
            return leader_member.user.fullname
        except StudyMember.DoesNotExist:
            return None

    def get_member_count(self, obj):
        return obj.studymember_set.count()


class StudyRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "description",
            "thumbnail_url",
            "type",
            "max_wait_member",
            "level",
            "gender",
            "category",
            "schedule",
            "start_time",
            "end_time",
            "member",
            "leader",
        ]

    def create(self, validated_data):
        return Study.objects.create(**validated_data)


class StudyLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ["id", "is_live"]

    def validate(self, attrs):
        # 요청 user 가져오기 (뷰에서 context로 넘긴 request.user)
        request = self.context.get("request")
        study = self.instance  # PATCH/PUT일 경우 instance, 즉 해당 Study 객체

        if not request or not hasattr(request, "user"):
            raise serializers.ValidationError("인증 정보가 없습니다.")

        # 리더가 아니면 에러
        if study.leader != request.user:
            raise serializers.ValidationError("스터디 리더만 방 활성화/비활성화가 가능합니다.")

        return attrs
