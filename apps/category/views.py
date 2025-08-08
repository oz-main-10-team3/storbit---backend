from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.category.models import Category
from apps.category.serializers import CategorySerializer


class CategoryListView(APIView):
    @extend_schema(
        summary="대분류 카테고리 목록 조회",
        description="대분류(최상위) 카테고리 리스트를 반환합니다.",
        responses={status.HTTP_200_OK: CategorySerializer(many=True)},
        tags=["category"],
    )
    def get(self, request: Request) -> Response:
        categories = Category.objects.filter(parent__isnull=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubCategoryListView(APIView):
    @extend_schema(
        summary="특정 대분류의 소분류 카테고리 조회",
        description="대분류 ID를 받아 해당 대분류의 소분류 카테고리를 반환합니다.",
        parameters=[
            {
                "name": "parent_id",
                "in": "query",
                "required": True,
                "description": "대분류 카테고리 ID",
                "schema": {"type": "integer"},
            }
        ],
        responses={
            status.HTTP_200_OK: CategorySerializer(many=True),
            status.HTTP_400_BAD_REQUEST: None,
        },
        tags=["category"],
    )
    def get(self, request: Request) -> Response:
        parent_id = request.GET.get("parent_id")
        if parent_id is None:
            return Response({"error": "parent_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        subcategories = Category.objects.filter(parent_id=parent_id)
        serializer = CategorySerializer(subcategories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
