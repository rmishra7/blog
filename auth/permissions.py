
from rest_framework import permissions


__all__ = [
    'IsNotAuthenticated',
]


class IsNotAuthenticated(permissions.BasePermission):

    """
    Allows access only to un-authenticated users.
    """

    def has_permission(self, request, view):
        return not (request.user and request.user.is_authenticated())
