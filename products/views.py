
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Q, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import Product, Category
from .form import ProductForm, ProductImageFormSet, CategoryForm

from orders.models import Order
from payments.models import Payment
from inventory.models import Inventory


def product_list(request):
    products = Product.objects.filter(
        is_active=True
    ).select_related("category")

    return render(
        request,
        "products/product_list.html",
        {"products": products}
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        is_active=True,
    )

    return render(
        request,
        "products/product_detail.html",
        {"product": product}
    )


def product_manager_required(user):
    return user.is_authenticated and user.is_product_manager


def get_revenue(start_date, end_date):
    start_datetime = timezone.make_aware(
        datetime.combine(start_date, time.min)
    )
    end_datetime = timezone.make_aware(
        datetime.combine(end_date, time.min)
    )

    result = Payment.objects.filter(
        status="successful",
        paid_at__isnull=False,
        paid_at__gte=start_datetime,
        paid_at__lt=end_datetime,
    ).aggregate(total=Sum("amount"))

    return result["total"] or Decimal("0.00")


@login_required
@user_passes_test(product_manager_required)
def owner_dashboard(request):
    today = timezone.localdate()

    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    tomorrow = today + timedelta(days=1)

    # Sales figures based on when payment was received
    today_revenue = get_revenue(today, tomorrow)
    weekly_revenue = get_revenue(week_start, tomorrow)
    monthly_revenue = get_revenue(month_start, tomorrow)

    # Order statistics
    total_orders = Order.objects.count()

    order_statuses = {
        "pending": Order.objects.filter(status="pending").count(),
        "confirmed": Order.objects.filter(status="confirmed").count(),
        "processing": Order.objects.filter(status="processing").count(),
        "shipped": Order.objects.filter(status="shipped").count(),
        "delivered": Order.objects.filter(status="delivered").count(),
        "cancelled": Order.objects.filter(status="cancelled").count(),
    }

    # Inventory statistics
    inventory_items = Inventory.objects.select_related("product")

    inventory_totals = inventory_items.aggregate(
        total_quantity=Sum("quantity"),
        total_reserved=Sum("reserved_quantity"),
    )

    total_stock = inventory_totals["total_quantity"] or 0
    reserved_stock = inventory_totals["total_reserved"] or 0
    available_stock = max(total_stock - reserved_stock, 0)

    low_stock_items = [
        item for item in inventory_items
        if item.is_low_stock
    ]

    out_of_stock_items = [
        item for item in inventory_items
        if item.is_out_of_stock
    ]

    # Product statistics
    all_products = Product.objects.select_related("category", "inventory")

    total_products = all_products.count()
    active_products = all_products.filter(is_active=True).count()
    inactive_products = all_products.filter(is_active=False).count()

    # Product search and filters
    products = all_products

    search_query = request.GET.get("q", "").strip()
    category_filter = request.GET.get("category", "")
    status_filter = request.GET.get("status", "")

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(sku__icontains=search_query)
            | Q(brand__icontains=search_query)
        )

    if category_filter:
        products = products.filter(category_id=category_filter)

    if status_filter == "active":
        products = products.filter(is_active=True)
    elif status_filter == "inactive":
        products = products.filter(is_active=False)

    # Last 30 days sales chart
    chart_start = today - timedelta(days=29)

    chart_start_datetime = timezone.make_aware(
        datetime.combine(chart_start, time.min)
    )

    chart_end_datetime = timezone.make_aware(
        datetime.combine(tomorrow, time.min)
    )

    daily_revenue = (
        Payment.objects.filter(
            status="successful",
            paid_at__isnull=False,
            paid_at__gte=chart_start_datetime,
            paid_at__lt=chart_end_datetime,
        )
        .annotate(payment_date=TruncDate("paid_at"))
        .values("payment_date")
        .annotate(revenue=Sum("amount"))
        .order_by("payment_date")
    )

    revenue_by_date = {
        item["payment_date"]: item["revenue"]
        for item in daily_revenue
    }

    sales_chart = []

    for day_number in range(30):
        chart_date = chart_start + timedelta(days=day_number)

        sales_chart.append({
            "date": chart_date.strftime("%d %b"),
            "revenue": float(
                revenue_by_date.get(chart_date, Decimal("0.00"))
            ),
        })

    context = {
        # Sales
        "today_revenue": today_revenue,
        "weekly_revenue": weekly_revenue,
        "monthly_revenue": monthly_revenue,
        "sales_chart": sales_chart,

        # Orders
        "total_orders": total_orders,
        "order_statuses": order_statuses,

        # Inventory
        "total_stock": total_stock,
        "reserved_stock": reserved_stock,
        "available_stock": available_stock,
        "low_stock_count": len(low_stock_items),
        "out_of_stock_count": len(out_of_stock_items),
        "low_stock_items": low_stock_items,

        # Products
        "products": products,
        "total_products": total_products,
        "active_products": active_products,
        "inactive_products": inactive_products,
        "categories": Category.objects.filter(is_active=True),

        # Filters
        "search_query": search_query,
        "category_filter": category_filter,
        "status_filter": status_filter,
    }

    return render(
        request,
        "products/owner/dashboard.html",
        context
    )


@login_required
@user_passes_test(product_manager_required)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        formset = ProductImageFormSet(
            request.POST,
            request.FILES,
            instance=form.instance,
        )

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                product = form.save()
                formset.instance = product
                formset.save()

            messages.success(request, "Product added successfully.")
            return redirect("products:owner_dashboard")

    else:
        form = ProductForm()
        formset = ProductImageFormSet(instance=form.instance)

    return render(
        request,
        "products/owner/product_form.html",
        {
            "form": form,
            "formset": formset,
            "page_title": "Add New Product",
        }
    )


@login_required
@user_passes_test(product_manager_required)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,
        )

        formset = ProductImageFormSet(
            request.POST,
            request.FILES,
            instance=product,
        )

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()

            messages.success(request, "Product updated successfully.")
            return redirect("products:owner_dashboard")

    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)

    return render(
        request,
        "products/owner/product_form.html",
        {
            "form": form,
            "formset": formset,
            "page_title": "Edit Product",
            "product": product,
        }
    )

@login_required
@user_passes_test(product_manager_required)
def category_list(request):
    categories = Category.objects.all().prefetch_related("products")

    return render(
        request,
        "products/owner/category_list.html",
        {"categories": categories}
    )


@login_required
@user_passes_test(product_manager_required)
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect("products:category_list")
    else:
        form = CategoryForm()

    return render(
        request,
        "products/owner/category_form.html",
        {
            "form": form,
            "page_title": "Add New Category",
        }
    )


@login_required
@user_passes_test(product_manager_required)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(
            request.POST,
            request.FILES,
            instance=category,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect("products:category_list")
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "products/owner/category_form.html",
        {
            "form": form,
            "page_title": "Edit Category",
            "category": category,
        }
    )


@login_required
@user_passes_test(product_manager_required)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        if category.products.exists():
            messages.error(
                request,
                "This category cannot be deleted because products are assigned to it."
            )
        else:
            category.delete()
            messages.success(request, "Category deleted successfully.")

        return redirect("products:category_list")

    return render(
        request,
        "products/owner/category_confirm_delete.html",
        {"category": category}
    )

