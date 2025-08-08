from django.urls import path

from apps.studies.serializers.study_application_serializers import StudyApplicationCreateAPIView

urlpatterns = [
    path("applications/", StudyApplicationCreateAPIView.as_view(), name="study-application-create"),
]