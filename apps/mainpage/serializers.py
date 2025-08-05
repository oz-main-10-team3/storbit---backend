from rest_framework import serializers

from .models import Study


class MainStudySerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    category = serializers.CharField(source="category.name", read_only=True)
    start_date = serializers.DateField(source="start_time", format="%Y-%m-%d")
    end_date = serializers.DateField(source="end_time", format="%Y-%m-%d")
    is_recruiting = serializers.SerializerMethodField()

    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "thumbnail_url",
            "description",
            "category",
            "start_date",
            "end_date",
            "is_recruiting",
            "is_favorited",
        ]

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.favorited_by.filter(id=user.id).exists()
        return False

    def get_is_recruiting(self, obj):
        return obj.status == "recruiting"
