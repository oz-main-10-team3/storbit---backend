from django.urls import path

from apps.studies.views import StudyDetailView

app_name = "studies"

urlpatterns = [
    path("studies/<int:id>/", StudyDetailView.as_view(), name="study-detail"),
]
