from django.urls import path

from apps.studies.views.missions import LeaderMissionCreateView
from apps.studies.views.study_favorite import StudyFavoriteAPIView
from apps.studies.views.study_favorite_list import MyStudyListView
from apps.studies.views.study_room import (
    StudyActiveAPIView,
    StudyDeactiveAPIView,
    StudyRoomCreateAPIView,
    StudyRoomDetailAPIView,
    StudyRoomListAPIView,
)
from apps.studies.views.studyrooms_application import StudyMemberAPIView
from apps.studies.views.studyrooms_apply import StudyApplyAPIView

urlpatterns = [
    path("study-rooms/", StudyRoomListAPIView.as_view(), name="studyroom-list"),
    path("study-rooms/create/", StudyRoomCreateAPIView.as_view(), name="studyroom-create"),
    path("study-rooms/<int:pk>/", StudyRoomDetailAPIView.as_view(), name="studyroom-detail"),
    path("stidy-rooms/lead/<int:study_id>/", LeaderMissionCreateView.as_view(), name="leadermission-create"),
    path("studies/<int:study_id>/apply/", StudyApplyAPIView.as_view(), name="study_apply"),
    path("studies/<int:study_id>/accept/<int:user_id>/", StudyMemberAPIView.as_view(), name="study_member_accept"),
    path("study-room/active/<int:study_id>", StudyActiveAPIView.as_view(), name="study_room_activate"),
    path("study-room/deactie/<int:study_id>", StudyDeactiveAPIView.as_view(), name="study_room_activate"),
    path("studies/<int:study_id>/favorite/", StudyFavoriteAPIView.as_view(), name="study_favorite"),
    path("my/favorites/", MyStudyListView.as_view(), name="my-favorites"),
]
