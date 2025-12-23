from django.shortcuts import render, get_object_or_404
from dicon_app.models import Product
from orders.models import Order
from orders.utils import notify_line_dummy

# Create your views here.
#成功・失敗で Order 作成 → 通知ダミー

def checkout(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # ✅ 注文（決済前の仮注文）を作る
    order = Order.objects.create(
        product=product,
        amount=product.price,
        status="pending",
    )

    return render(request, "payments/checkout.html", {"product": product, "order": order})


def success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # ✅ 成功に更新
    order.status = "success"
    order.save()

    # ✅ LINE通知ダミー（print される）
    message = notify_line_dummy(order, order.product, order.status)

    return render(request, "payments/success.html", {"order": order, "product": order.product, "message": message})


def cancel(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # ✅ 失敗に更新
    order.status = "cancel"
    order.save()

    # ✅ LINE通知ダミー（print される）
    message = notify_line_dummy(order, order.product, order.status)

    return render(request, "payments/cancel.html", {"order": order, "product": order.product, "message": message})
