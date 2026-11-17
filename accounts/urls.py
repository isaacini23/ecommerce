
from django.urls import path

from . import views

app_name = "accounts"


urlpatterns = [
    # Customer registration and account
    path("register/", views.register, name="register"),
    path("", views.account, name="account"),
    path("login/", views.customer_login, name="login"),
    path("logout/", views.customer_logout, name="logout"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # Owner registration
    path(
    "owner/register/<uuid:token>/",
    views.owner_register,
    name="owner_register",),

    # Password change
    path(
        "password/change/",
        views.CustomerPasswordChangeView.as_view(),
        name="change_password",
    ),

    # Password reset
    path(
        "password/reset/",
        views.CustomerPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password/reset/done/",
        views.CustomerPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        views.CustomerPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/reset/complete/",
        views.CustomerPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
