from django.urls import path

from apps.category.views import CategoryListView, SubCategoryListView

app_name = "apps.category"

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/sub/", SubCategoryListView.as_view(), name="subcategory-list"),
]
