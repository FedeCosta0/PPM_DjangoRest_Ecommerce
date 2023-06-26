from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'destroy']:
            return bool(request.user.is_authenticated and request.user.is_admin)
        elif view.action in ['retrieve', 'update', 'partial_update']:
            return bool(request.user.is_authenticated)
        elif view.action == 'create':
            return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update']:
            return bool(request.user == obj or request.user.is_admin)


class UserAddressPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return bool(request.user == obj.user or request.user.is_admin)
