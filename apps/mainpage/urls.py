from django.urls import path

from apps.mainpage.views import MainStudyListAPIView

urlpatterns = [
    path("main-studies/", MainStudyListAPIView.as_view(), name="main-study-list"),
]
