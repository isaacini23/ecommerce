
from django.urls import path
from .views import (
    product_list,
    product_detail,
    owner_dashboard,
    product_create,
    product_edit,
    category_list,
    category_create,
    category_edit,
    category_delete,
)

app_name = "products"

urlpatterns = [
    path("", product_list, name="list"),

    # Owner dashboard
    path("owner/dashboard/", owner_dashboard, name="owner_dashboard"),

    # Owner product management
    path("owner/products/add/", product_create, name="product_create"),
    path("owner/products/<int:pk>/edit/", product_edit, name="product_edit"),

    # Owner category management
    path("owner/categories/", category_list, name="category_list"),
    path("owner/categories/add/", category_create, name="category_create"),
    path("owner/categories/<int:pk>/edit/", category_edit, name="category_edit"),
    path("owner/categories/<int:pk>/delete/", category_delete, name="category_delete"),

    # Product details
    path("<slug:slug>/", product_detail, name="detail"),
]
