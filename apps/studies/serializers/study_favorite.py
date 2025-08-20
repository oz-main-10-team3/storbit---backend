from rest_framework import serializers

from apps.studies.models import Study, StudyFavorite


class StudyFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyFavorite
        fields = ["id", "user", "study", "is_active"]
