from django.urls import path
from .views import RoomView, SingleRoomView, MessageView, SingleMessageView

urlpatterns = [
    path("rooms/", RoomView.as_view(), name="room-list"),
    path("rooms/<int:pk>/", SingleRoomView.as_view(), name="room-detail"),
    path("messages/", MessageView.as_view(), name="message-list"),
    path("messages/<int:pk>/", SingleMessageView.as_view(), name="message-detail"),
]
