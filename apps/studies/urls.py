from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.studies.views.study_room import StudyRoomViewSet

router = DefaultRouter()
router.register(r"study-rooms", StudyRoomViewSet, basename="studyroom")

urlpatterns = [
    path("", include(router.urls)),
]
