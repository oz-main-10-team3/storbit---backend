from django.urls import path
from apps.studies.views import StudyDetailView
from apps.studies.views.vote import VoteCreateAPIView


app_name = "studies"

urlpatterns = [
    path("studies/<int:id>/", StudyDetailView.as_view(), name="study-detail"),
    path("votes/", VoteCreateAPIView.as_view(), name="vote-create"),
]
