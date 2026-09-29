from django.urls import path
from .views import (
    add_to_cart,
    cart_detail,
    update_cart_item,
    remove_cart_item,
)

app_name = "cart"

urlpatterns = [
    path("", cart_detail, name="detail"),
    path("add/<int:product_id>/", add_to_cart, name="add"),
    path(
        "update/<int:item_id>/",
        update_cart_item,
        name="update",
    ),
    path(
        "remove/<int:item_id>/",
        remove_cart_item,
        name="remove",
    ),
]