from rest_framework import permissions


class ShoppingSessionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return bool(request.user.is_authenticated and request.user.is_admin)
        elif view.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return bool(request.user == obj.user or request.user.is_admin)


class CartProductPermission(permissions.BasePermission):
    pass
