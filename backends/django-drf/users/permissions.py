from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsAuthenticated() and (obj.user == request.user)
