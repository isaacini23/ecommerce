from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from .models import Cart, CartItem


@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(
            Product,
            id=product_id,
            is_active=True
        )

        quantity = int(request.POST.get("quantity", 1))

        if quantity < 1:
            quantity = 1

        # Get the product inventory
        try:
            inventory = product.inventory
        except Exception:
            inventory = None

        # Make sure the product has inventory
        if inventory is None or inventory.is_out_of_stock:
            messages.error(
                request,
                "This product is currently out of stock."
            )
            return redirect("products:detail", product.slug)

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        # Calculate the new quantity
        new_quantity = quantity

        if not created:
            new_quantity = cart_item.quantity + quantity

        # Check available stock
        if new_quantity > inventory.available_quantity:
            messages.error(
                request,
                f"Only {inventory.available_quantity} units are available."
            )
            return redirect("products:detail", product.slug)

        cart_item.quantity = new_quantity
        cart_item.save()

        return redirect("cart:detail")

    return redirect("products:list")


@login_required
def update_cart_item(request, item_id):
    if request.method == "POST":
        cart = get_object_or_404(
            Cart,
            user=request.user
        )

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart=cart
        )

        quantity = int(request.POST.get("quantity", 1))

        if quantity < 1:
            quantity = 1

        # Get inventory
        try:
            inventory = cart_item.product.inventory
        except Exception:
            inventory = None

        # Check inventory availability
        if inventory is None:
            messages.error(
                request,
                "This product is no longer available."
            )

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({
                    "success": False,
                    "message": "This product is no longer available."
                }, status=400)

            return redirect("cart:detail")

        if quantity > inventory.available_quantity:
            message = (
                f"Only {inventory.available_quantity} units are available."
            )

            messages.error(request, message)

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({
                    "success": False,
                    "message": message
                }, status=400)

            return redirect("cart:detail")

        cart_item.quantity = quantity
        cart_item.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "item_total": str(cart_item.total_price),
                "cart_total": str(cart.total_price),
                "quantity": cart_item.quantity,
            })

    return redirect("cart:detail")
@login_required
def remove_cart_item(request, item_id):
    if request.method == "POST":
        cart = get_object_or_404(
            Cart,
            user=request.user
        )

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart=cart
        )

        cart_item.delete()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "cart_total": str(cart.total_price),
                "total_items": cart.total_items,
            })

    return redirect("cart:detail")

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "cart/cart_detail.html",
        {
            "cart": cart,
        }
    )