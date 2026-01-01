from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Order

@login_required
def order_list(request):
    orders = Order.objects.select_related("product__shop").order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})

@login_required
def order_detail(request, order_pk):
    order = get_object_or_404(
        Order.objects.select_related("product__shop"),
        pk=order_pk
    )
    shop = order.product.shop
    return render(request, "orders/order_detail.html", {
        "order": order,
        "shop": shop,
    })
