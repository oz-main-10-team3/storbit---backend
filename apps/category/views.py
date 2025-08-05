from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from apps.category.models import Category
from apps.category.serializers import CategorySerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer

    @extend_schema(
        summary="대분류 카테고리 목록 조회",
        tags=["category"],
        responses=CategorySerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubCategoryListView(ListAPIView):
    serializer_class = CategorySerializer

    @extend_schema(
        summary="특정 대분류의 소분류 카테고리 조회",
        tags=["category"],
        responses=CategorySerializer(many=True),
    )
    def get_queryset(self):
        parent_id = self.kwargs.get("category_id")
        return Category.objects.filter(parent_id=parent_id)
