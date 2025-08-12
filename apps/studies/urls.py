from rest_framework.routers import DefaultRouter

from apps.studies.views.study_room import StudyRoomViewSet

router = DefaultRouter()
router.register(r"studyrooms", StudyRoomViewSet, basename="studyroom")

urlpatterns = router.urls
