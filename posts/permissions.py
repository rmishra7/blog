
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope


class ManualGetAuthentication(TokenHasReadWriteScope):

    def has_permission(self, request, view):
        if view.request.method == "GET":
            return True
        if view.request.user.is_anonymous():
            return False
        else:
            return True
