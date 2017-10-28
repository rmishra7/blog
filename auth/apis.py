
from django.contrib import auth
from django.utils import timezone
from django.conf import settings

from rest_framework import generics, response, status, serializers
from oauth2_provider import settings as oauth2_settings
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from datetime import timedelta
from oauthlib import common

from .permissions import IsNotAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, ProfileMiniSerializer


class RegisterApi(generics.CreateAPIView):
    """
    api to signup/register user
    """
    permission_classes = (IsNotAuthenticated, )
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(serializer.validated_data["password"])
        instance.save()


class LoginApi(generics.GenericAPIView):
    """
    api to authenticate user
    """
    permission_classes = (IsNotAuthenticated, )
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth.login(request, serializer.instance)
        data = {}
        access_token = self.oauth_validate(request.user)
        data['user'] = ProfileMiniSerializer(request.user).data
        data['expires_in'] = oauth2_settings.DEFAULTS["ACCESS_TOKEN_EXPIRE_SECONDS"]
        data['token_type'] = 'Bearer'
        data['scope'] = access_token.scope
        data['refresh_token'] = access_token.refresh_token.token
        data['authorization_token'] = access_token.token
        return response.Response(data=data, status=status.HTTP_200_OK)

    def oauth_validate(self, user):
        try:
            application = Application.objects.get(client_id=settings.CLIENT_ID, client_secret=settings.SECRET_ID)
            expires = timezone.now() + timedelta(seconds=oauth2_settings.DEFAULTS["ACCESS_TOKEN_EXPIRE_SECONDS"])
            access_token = AccessToken(
                user=user,
                scope='read write groups',
                expires=expires,
                token=common.generate_token(),
                application=application
            )
            access_token.save()
            refresh_token = RefreshToken(
                user=user,
                token=common.generate_token(),
                application=application,
                access_token=access_token
            )
            refresh_token.save()
            return access_token
        except:
            raise serializers.ValidationError({'error': 'something went wrong.'})


class LogOutApi(generics.GenericAPIView):
    """
    api to logout/unauthenticate user
    """
    permission_classes = [TokenHasReadWriteScope, ]

    def get(self, request, *args, **kwargs):
        application = Application.objects.get(client_id=settings.CLIENT_ID, client_secret=settings.SECRET_ID)
        token = AccessToken.objects.filter(token=request.META['HTTP_AUTHORIZATION'].split(" ")[1], application=application)
        token[0].revoke()
        return response.Response(data="Logout successfully", status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveAPIView):
    """
    api to return user profile detail
    """
    permission_classes = [TokenHasReadWriteScope, ]
    serializer_class = ProfileMiniSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
