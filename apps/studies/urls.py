from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.studies.views.studyrooms import StudyViewSet

router = DefaultRouter()
router.register(r"study-rooms", StudyViewSet, basename="studyroom")

urlpatterns = [
    path("", include(router.urls)),
]
