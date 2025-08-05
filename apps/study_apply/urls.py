from django.urls import include, path

from apps.study_apply.views import StudyApplicationCreateView

urlpatterns = [
    path("<int:study_id>/applications/", StudyApplicationCreateView.as_view(), name="study-application"),
]
