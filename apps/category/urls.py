from django.urls import path

from .views import CategoryListView, SubCategoryListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:category_id>/subcategories/", SubCategoryListView.as_view(), name="subcategory-list"),
]
