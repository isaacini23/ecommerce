
from django.urls import path
from .views import (
    product_list,
    product_detail,
    owner_dashboard,
    product_create,
    product_edit,
)

app_name = "products"

urlpatterns = [
    path("", product_list, name="list"),
    path("owner/dashboard/", owner_dashboard, name="owner_dashboard"),
    path("owner/products/add/", product_create, name="product_create"),
    path("owner/products/<int:pk>/edit/", product_edit, name="product_edit"),
    path("<slug:slug>/", product_detail, name="detail"),
]
