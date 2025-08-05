from django.urls import path

from apps.studies.views import StudyDetailView

urlpatterns = [
    path("studies/<int:id>/", StudyDetailView.as_view(), name="study-detail"),
]
