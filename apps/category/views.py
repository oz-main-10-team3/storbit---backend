from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.category.models import Category
from apps.category.serializers import CategorySerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer

    @extend_schema(
        tags=["카테고리"],
        summary="대분류 카테고리 목록 조회",
        description="대분류(최상위) 카테고리 리스트를 반환합니다.",
        responses={200: CategorySerializer(many=True)},
    ) # <-- 닫는 괄호 추가
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubCategoryListView(APIView):
    @extend_schema(
        tags=["카테고리"],
        summary="특정 대분류의 소분류 카테고리 조회",
        description="대분류 ID를 받아 해당 대분류의 소분류 카테고리를 반환합니다.",
        parameters=[
            OpenApiParameter(
                name="parent_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="대분류(부모) 카테고리의 ID",
                required=True,
            ),
        ],
        responses={200: CategorySerializer(many=True)},
    )
    def get(self, request):
        parent_id = request.GET.get("parent_id")
        if parent_id is None:
            return Response({"error": "parent_id is required"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            parent_id = int(parent_id)
        except (ValueError, TypeError):
            return Response({"error": "parent_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        subcategories = Category.objects.filter(parent_id=parent_id)
        serializer = CategorySerializer(subcategories, many=True)
        return Response(serializer.data)