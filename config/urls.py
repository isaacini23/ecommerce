from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

LOGIN_URL = "/accounts/login/"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("products/", include("products.urls")),
    path("cart/", include("cart.urls")),
    path("accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )