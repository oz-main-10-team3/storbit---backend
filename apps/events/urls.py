# apps/events/urls.py
from django.urls import path

from .views import (
    AdminEventCreateView,
    AdminEventDeleteView,
    AdminEventUpdateView,
    EventDetailView,
    EventListView,
)

urlpatterns = [
    # 유저
    path("events/", EventListView.as_view(), name="event-list"),
    path("events/<int:event_id>/", EventDetailView.as_view(), name="event-detail"),
    # 어드민
    path("admin/events/", AdminEventCreateView.as_view(), name="admin-event-create"),
    path("admin/events/<int:event_id>/", AdminEventUpdateView.as_view(), name="admin-event-update"),
    path("admin/events/<int:event_id>/delete/", AdminEventDeleteView.as_view(), name="admin-event-delete"),
]
