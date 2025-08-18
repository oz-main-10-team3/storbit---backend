from django.urls import re_path

from apps.studies.consumers import StudyConsumer

study_urlpatterns = [
    re_path(r"^ws/study/(?P<study_id>\d+)/$", StudyConsumer.as_asgi()),
]
