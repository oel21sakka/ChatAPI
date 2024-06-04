from rest_framework.permissions import BasePermission


class IsRoomUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return request.user in obj.users.all()
        return obj.admin == request.user


class IsMessageOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user == obj.user
