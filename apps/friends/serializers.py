from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Friend, FriendRequest

User = get_user_model()


class FriendRequestCreateSerializer(serializers.ModelSerializer):
    to_user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="to_user", write_only=True)

    class Meta:
        model = FriendRequest
        fields = ["id", "to_user_id", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]

    def create(self, validated_data: dict[str, Any]) -> FriendRequest:
        from_user = self.context["request"].user
        to_user = validated_data["to_user"]

        if from_user == to_user:
            raise serializers.ValidationError("자기 자신에게 친구 요청은 보낼 수 없습니다.")

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise serializers.ValidationError("이미 친구 요청을 보냈습니다.")

        return FriendRequest.objects.create(from_user=from_user, to_user=to_user)


class FriendRequestResponseSerializer(serializers.Serializer):
    accept = serializers.BooleanField()

    def save(self, **kwargs: Any) -> FriendRequest:
        friend_request: FriendRequest = self.context["friend_request"]
        friend_request.status = "accepted" if self.validated_data["accept"] else "rejected"
        friend_request.responded_at = kwargs.get("responded_at")
        friend_request.save()

        if friend_request.status == "accepted":
            Friend.objects.create(user=friend_request.from_user, friend=friend_request.to_user)
            Friend.objects.create(user=friend_request.to_user, friend=friend_request.from_user)

        return friend_request
