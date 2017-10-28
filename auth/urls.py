
from django.conf.urls import url

from auth import apis

urlpatterns = [
    url(r"signup/$", apis.RegisterApi.as_view(), name="auth_signup"),
    url(r"login/$", apis.LoginApi.as_view(), name="auth_login"),
    url(r"logout/$", apis.LogOutApi.as_view(), name="auth_logoout"),
    url(r"user/$", apis.UserDetail.as_view(), name="auth_user_detail")
]
