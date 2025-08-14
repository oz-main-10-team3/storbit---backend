from django.contrib.auth import get_user_model
from rest_framework import serializers

<<<<<<< HEAD
from apps.studies.models import StudyMember, Study
=======
from apps.studies.models import StudyMember, StudyRole, StudyRoom
>>>>>>> 1b2b0fa (all change code)

User = get_user_model()


class StudyRoomSerializer(serializers.ModelSerializer):
    leader_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
<<<<<<< HEAD
        model = Study
=======
        model = StudyRoom
>>>>>>> 1b2b0fa (all change code)
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
<<<<<<< HEAD
            leader_member = obj.studymember_set.get(role=StudyMember.Role.MASTER)
=======
            leader_member = obj.studymember_set.get(role=StudyRole.MASTER)
>>>>>>> 1b2b0fa (all change code)
            return leader_member.user.username
        except StudyMember.DoesNotExist:
            return None

    def get_member_count(self, obj):
        return obj.studymember_set.count()


class StudyRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = Study
=======
        model = StudyRoom
>>>>>>> 1b2b0fa (all change code)
        fields = [
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
        ]

    def create(self, validated_data):
<<<<<<< HEAD
        return Study.objects.create(**validated_data)
=======
        return StudyRoom.objects.create(**validated_data)
>>>>>>> 1b2b0fa (all change code)


class TransferOwnerSerializer(serializers.Serializer):
    new_owner_id = serializers.IntegerField(help_text="새로운 방장으로 위임할 사용자의 ID")

    def validate_new_owner_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("지정한 사용자가 존재하지 않습니다.")
        return value
