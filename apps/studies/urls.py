from django.urls import path

from apps.studies.views.study_room import (
    StudyRoomCreateAPIView,
    StudyRoomDetailAPIView,
    StudyRoomListAPIView,
)

urlpatterns = [
    path("study-rooms/", StudyRoomListAPIView.as_view(), name="studyroom-list"),
    path("study-rooms/create/", StudyRoomCreateAPIView.as_view(), name="studyroom-create"),
    path("study-rooms/<int:pk>/", StudyRoomDetailAPIView.as_view(), name="studyroom-detail"),
]
