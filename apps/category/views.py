from unicodedata import category

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.category.models import Category
from apps.category.serializers import CategorySerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_summary="대분류 카테고리 목록 조회",
        operation_description="대분류(최상위) 카테고리 리스트를 반환합니다.",
        responses={200: CategorySerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubCategoryListView(APIView):
    @swagger_auto_schema(
        operation_summary="특정 대분류의 소분류 카테고리 조회",
        operation_description="대분류 ID를 받아 해당 대분류의 소분류 카테고리를 반환합니다.",
        manual_parameters=[
            openapi.Parameter("parent_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={200: CategorySerializer(many=True)},
    )
    def get(self, request):
        parent_id = request.GET.get("parent_id")
        if parent_id is None:
            return Response({"error": "parent_id is required"}, status=400)
        subcategories = Category.objects.filter(parent_id=parent_id)
        serializer = CategorySerializer(subcategories, many=True)
        return Response(serializer.data)
