
from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone

from django.contrib.auth.admin import UserAdmin

from .models import User, OwnerInvitation


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_product_manager",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_product_manager",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
    )

    ordering = ("email",)

    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),
        ("Personal Information", {
            "fields": ("first_name", "last_name", "phone")
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_product_manager",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "phone",
                "is_active",
                "is_product_manager",
                "is_staff",
            ),
        }),
    )


@admin.register(OwnerInvitation)
class OwnerInvitationAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "created_at",
        "expires_at",
        "invitation_status",
        "is_active",
    )

    list_filter = (
        "is_active",
        "created_at",
        "expires_at",
    )

    search_fields = ("email",)

    readonly_fields = (
        "token",
        "created_at",
        "used_at",
        "created_by",
        "invitation_link",
    )

    fields = (
        "email",
        "expires_at",
        "is_active",
        "created_by",
        "token",
        "created_at",
        "used_at",
        "invitation_link",
    )

    ordering = ("-created_at",)

    actions = ("deactivate_invitations",)

    @admin.display(description="Status")
    def invitation_status(self, obj):
        if obj.used_at:
            return "Used"

        if not obj.is_active:
            return "Deactivated"

        if timezone.now() >= obj.expires_at:
            return "Expired"

        return "Active"

    @admin.display(description="Registration link")
    def invitation_link(self, obj):
        if not obj or not obj.pk:
            return "Save the invitation first to generate its link."

        path = reverse(
            "accounts:owner_register",
            kwargs={"token": obj.token},
        )

        url = self.request.build_absolute_uri(path)

        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer">'
            'Open registration link</a><br><br>'
            '<input type="text" value="{}" readonly '
            'style="width:100%;max-width:600px;padding:8px;" '
            'onclick="this.select();">',
            url,
            url,
        )

    def get_form(self, request, obj=None, **kwargs):
        self.request = request
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    @admin.action(description="Deactivate selected invitations")
    def deactivate_invitations(self, request, queryset):
        updated = queryset.filter(
            used_at__isnull=True
        ).update(is_active=False)

        self.message_user(
            request,
            f"{updated} invitation(s) deactivated.",
            messages.SUCCESS,
        )
