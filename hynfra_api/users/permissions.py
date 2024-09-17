from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_admin()

class IsStandardUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_standard_user()

class IsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_guest()