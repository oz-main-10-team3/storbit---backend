from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 12  # 또는 원하는 수치
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(
            {
                "page": self.page.number,
                "has_next": self.page.has_next(),
                "results": data,
            }
        )
