from rest_framework import permissions


class ProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return bool(request.user.is_authenticated and request.user.is_admin)


class ProductCategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return bool(request.user.is_authenticated and request.user.is_admin)


class ProductInventoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)


class DiscountPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)
