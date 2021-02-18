from rest_framework.permissions import BasePermission, SAFE_METHODS

from pages.models import ProductCategory


class OwnerWritePerm(BasePermission):
    message = 'Manipulating objects is restricted to owner only'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.belongs_to == request.user


class OwnsCategoryPerm(BasePermission):
    message = "The specified category belongs to someone else"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        category = request.data.get('category', None)
        if category:
            if ProductCategory.objects.get(pk=category).belongs_to != request.user:
                return False
        return True
