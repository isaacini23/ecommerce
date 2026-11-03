from django.urls import path

from . import views
app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.account, name="account"),
    path("login/", views.customer_login, name="login"),
    path("logout/", views.customer_logout, name="logout"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("password/change/", views.CustomerPasswordChangeView.as_view(), name="change_password"),
    path("password/reset/", views.CustomerPasswordResetView.as_view(), name="password_reset",),
    path("password/reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done",),

path(
    "password/reset/confirm/<uidb64>/<token>/",
    views.CustomerPasswordResetConfirmView.as_view(),
    name="password_reset_confirm",
),

path(
    "password/reset/complete/",
    views.PasswordResetCompleteView.as_view(),
    name="password_reset_complete",
),
]