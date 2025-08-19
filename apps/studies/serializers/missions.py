from rest_framework import serializers

from apps.studies.models import DailyMission, LeaderMission


class LeaderMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderMission
        fields = ["final_goal", "common_mission"]


class DailyMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMission
        fields = "__all__"
