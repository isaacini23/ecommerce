from django.contrib import admin
from .models import Address, Order, OrderItem


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "user",
        "phone",
        "city",
        "state",
        "country",
        "is_default",
        "created_at",
    )

    list_filter = (
        "country",
        "state",
        "is_default",
    )

    search_fields = (
        "full_name",
        "phone",
        "user__email",
        "city",
        "state",
        "address_line_1",
    )

    ordering = ("-created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = (
        "product",
        "product_name",
        "unit_price",
        "quantity",
        "total_price",
    )
    readonly_fields = (
        "total_price",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "payment_status",
        "subtotal",
        "shipping_fee",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [OrderItemInline]

    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product_name",
        "unit_price",
        "quantity",
        "total_price",
    )

    search_fields = (
        "order__order_number",
        "product_name",
        "product__name",
        "product__sku",
    )

    readonly_fields = (
        "total_price",
    )