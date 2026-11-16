
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db import transaction
from django.utils import timezone

from .models import OwnerInvitation

from .forms import (
    CustomerProfileForm,
    CustomerRegistrationForm,
    OwnerRegistrationForm,
)


def customer_login(request):
    if request.user.is_authenticated:
        if request.user.is_product_manager:
            return redirect("products:owner_dashboard")

        return redirect("accounts:account")

    error = None

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.is_product_manager:
                return redirect("products:owner_dashboard")

            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("accounts:account")

        error = "Invalid email or password."

    return render(
        request,
        "accounts/login.html",
        {"error": error}
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:account")

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("accounts:account")
    else:
        form = CustomerRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )



def owner_register(request, token):
    if request.user.is_authenticated:
        if request.user.is_product_manager:
            return redirect("products:owner_dashboard")

        return redirect("accounts:account")

    if request.method == "POST":
        with transaction.atomic():
            invitation = (
                OwnerInvitation.objects
                .select_for_update()
                .filter(token=token)
                .first()
            )

            if not invitation or not invitation.is_valid:
                return render(
                    request,
                    "accounts/owner_invitation_invalid.html"
                )

            form = OwnerRegistrationForm(
                request.POST,
                invitation=invitation
            )

            if form.is_valid():
                user = form.save(commit=False)
                user.save()

                invitation.used_at = timezone.now()
                invitation.is_active = False
                invitation.save(
                    update_fields=["used_at", "is_active"]
                )

                login(request, user)

                return redirect("products:owner_dashboard")

    else:
        invitation = OwnerInvitation.objects.filter(
            token=token
        ).first()

        if not invitation or not invitation.is_valid:
            return render(
                request,
                "accounts/owner_invitation_invalid.html"
            )

        form = OwnerRegistrationForm(
            invitation=invitation
        )

    return render(
        request,
        "accounts/owner_register.html",
        {"form": form}
    )

@login_required
def account(request):
    return render(
        request,
        "accounts/account.html"
    )


def customer_logout(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomerProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect("accounts:account")
    else:
        form = CustomerProfileForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {"form": form}
    )


class CustomerPasswordChangeView(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("accounts:account")


class CustomerPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomerPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

class CustomerPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomerPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"