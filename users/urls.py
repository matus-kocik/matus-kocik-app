from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import ActivateAccountView, UserLoginView, UserRegisterView

urlpatterns = [
    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),
    path(
        "register/",
        UserRegisterView.as_view(),
        name="register",
    ),
    path(
        "activate/<uidb64>/<token>/",
        ActivateAccountView.as_view(),
        name="activate",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page="/"),
        name="logout",
    ),
]
