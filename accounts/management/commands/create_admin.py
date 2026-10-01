import os

from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "Create or update the production admin user."

    def handle(self, *args, **options):
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not email or not password:
            self.stdout.write(
                self.style.ERROR(
                    "DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD "
                    "must be set."
                )
            )
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": "Admin",
                "last_name": "User",
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user {email} created successfully."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user {email} already existed. Password and permissions updated."
                )
            )
