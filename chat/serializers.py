from rest_framework import serializers
from .models import Room, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["user"]

    def update(self, instance, validated_data):
        data = {}
        if "content" in validated_data:
            data["content"] = validated_data.pop("content")
        return super().update(instance, data)

    def validate(self, attrs):
        user = self.context["request"].user
        room = attrs.get("room")

        if room and user not in room.users.all():
            raise serializers.ValidationError(
                "User must be part of the room to create a message."
            )
        return attrs


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

    def to_representation(self, instance):
        users = UserSerializer(instance.users, many=True).data
        data = super().to_representation(instance)
        data["users"] = users
        return data

    def validate(self, attrs):
        admin = attrs.get("admin", self.context["request"].user)
        users = list(attrs.get("users", []))

        if admin not in users:
            raise serializers.ValidationError("Admin must be a user in the room.")
        return attrs
