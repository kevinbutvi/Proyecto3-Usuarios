from django.urls import path
from . import views

app_name = "users_app"

urlpatterns = [
    path(
        'register/',
        views.UserRegisterView.as_view(),
        name="user-register",
        ),
    path(
        'login/',
        views.LoginUser.as_view(),
        name="login-user",
        ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name="logout-user",
        ),
    path(
        'update/',
        views.UpdatePasswordView.as_view(),
        name="update-user",
        ),
    path(
        'user-verfication/<pk>',
        views.CodVerificationView.as_view(),
        name="user-verification",
        ),
]