from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    fields = ("product", "quantity", "total_price")
    readonly_fields = ("total_price",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "total_items",
        "total_price",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__email",
    )

    readonly_fields = (
        "total_items",
        "total_price",
    )

    inlines = [CartItemInline]

    ordering = ("-updated_at",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "product",
        "quantity",
        "total_price",
    )

    search_fields = (
        "cart__user__email",
        "product__name",
        "product__sku",
    )

    readonly_fields = (
        "total_price",
    )