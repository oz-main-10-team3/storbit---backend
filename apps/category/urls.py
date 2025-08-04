from django.urls import path

from apps.category.views import CategoryListView, SubCategoryListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/sub/", SubCategoryListView.as_view(), name="subcategory-list"),
]
