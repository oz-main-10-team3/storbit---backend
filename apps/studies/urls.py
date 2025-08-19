from django.urls import path

from apps.studies.views.missions import LeaderMissionCreateView
from apps.studies.views.study_room import (
    StudyRoomCreateAPIView,
    StudyRoomDetailAPIView,
    StudyRoomListAPIView,
)
from apps.studies.views.studyrooms_apply import StudyApplyAPIView

urlpatterns = [
    path("study-rooms/", StudyRoomListAPIView.as_view(), name="studyroom-list"),
    path("study-rooms/create/", StudyRoomCreateAPIView.as_view(), name="studyroom-create"),
    path("study-rooms/<int:pk>/", StudyRoomDetailAPIView.as_view(), name="studyroom-detail"),
    path("stidy-rooms/lead/<int:study_id>/", LeaderMissionCreateView.as_view(), name="leadermission-create"),
    path("studies/<int:study_id>/apply/", StudyApplyAPIView.as_view(), name="study_apply"),
]
