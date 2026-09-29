from django.shortcuts import render
from products.models import Product


def home(request):
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    )[:8]

    return render(
        request,
        "core/home.html",
        {
            "featured_products": featured_products,
        }
    )