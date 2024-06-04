from rest_framework import generics, filters, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from .permissions import IsRoomUserOrAdmin, IsMessageOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class RoomView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(users=user).prefetch_related("users")

    def perform_create(self, serializer):
        users = list(serializer.validated_data.get("users", []))
        if self.request.user not in users:
            users.append(self.request.user)
        serializer.save(admin=self.request.user, users=users)


class SingleRoomView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all().prefetch_related("users")
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsRoomUserOrAdmin]


class MessageView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["content"]
    filterset_fields = ["room", "user"]

    def get_queryset(self):
        user_rooms = self.request.user.rooms.all()
        return Message.objects.filter(room__in=user_rooms)

    def perform_create(self, serializer):
        room = serializer.validated_data.get("room")
        if self.request.user not in room.users.all():
            raise serializers.ValidationError(
                "User must be part of the room to create a message."
            )
        serializer.save(user=self.request.user)


class SingleMessageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwnerOrReadOnly]
