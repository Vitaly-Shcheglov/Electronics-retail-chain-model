from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Разрешение для проверки, является ли пользователь модератором.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь разрешение на доступ к представлению.
        """
        return request.user.groups.filter(name="Moderators").exists()
