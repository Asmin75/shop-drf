from rest_framework import permissions


# class IsAllowedToWrite(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.user_type == "User"

class IsOwnerOrReadonly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.user_type == "('Agent',)"


class IsAllowedToRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "('Agent',)"

