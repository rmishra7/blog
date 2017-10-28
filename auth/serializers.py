
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib import auth

from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password")


class AuthMixin(object):
    """
    authenticate user provided credentiatials
    """
    message = {
        "invalid": _("Invalid Details. Please check the Username-Password combination."),
        "disabled": _("This account is not active"),
    }

    def user_credentials(self, attrs):
        credentials = {}
        credentials["username"] = attrs["username"].lower()
        credentials["password"] = attrs["password"]
        return credentials

    def validate_user_credentials(self, data):
        user = auth.authenticate(**self.user_credentials(data))
        if user:
            if not user.is_active:
                raise serializers.ValidationError(self.message["disabled"])
        else:
            raise serializers.ValidationError(self.message["invalid"])
        self.instance = user
        return user


class LoginSerializer(serializers.Serializer, AuthMixin):

    username = serializers.CharField(max_length=80)
    password = serializers.CharField(max_length=80)

    def validate(self, attrs):
        self.validate_user_credentials(attrs)
        return attrs


class ProfileMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
