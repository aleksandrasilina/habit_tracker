from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    """Проверяет, является ли пользователь создателем привычки."""

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False
