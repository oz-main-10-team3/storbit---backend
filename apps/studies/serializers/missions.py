from urllib import request

from rest_framework import serializers

from apps.studies.models import DailyMission, LeaderMission, Study


class LeaderMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderMission
        fields = ["id", "final_goal", "common_mission"]


class DailyMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMission
        fields = "__all__"
