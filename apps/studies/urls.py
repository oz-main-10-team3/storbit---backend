from django.urls import path

from apps.studies.views.application_views import StudyApplicationCreateAPIView

urlpatterns = [
    path("applications/", StudyApplicationCreateAPIView.as_view(), name="study-application-create"),
]
