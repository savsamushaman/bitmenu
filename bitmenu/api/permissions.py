from rest_framework.permissions import BasePermission, SAFE_METHODS


class OwnerWritePerm(BasePermission):
    message = 'Manipulating objects is restricted to owner only'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.belongs_to == request.user

