from django.urls import path

from .views import FriendRequestCreateAPIView, FriendRequestRespondAPIView

app_name = "apps.friends"

urlpatterns = [
    path("friends/", FriendRequestCreateAPIView.as_view(), name="friend-request-create"),
    path(
        "friends/requests/<int:request_id>/respond/",
        FriendRequestRespondAPIView.as_view(),
        name="friend-request-respond",
    ),
]
