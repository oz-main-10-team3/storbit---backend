from django.urls import path

from apps.studies.views.study_application_view import (
    StudyApplicationCreateAPIView,
)

urlpatterns = [
    path("applications/", StudyApplicationCreateAPIView.as_view(), name="study-application-create"),
]
