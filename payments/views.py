# payments/views.py（このファイルを丸ごと上書き）

from django.shortcuts import render, get_object_or_404
from dicon_app.models import Product, Set
from orders.models import Order

# セット購入で作った注文IDたちを一時的に束ねる（DB変更なしの最短ルート）
SESSION_KEY_SET_ORDER_IDS = "checkout_set_order_ids"


# --------------------
# 1) 単品購入（既存）
# --------------------
def checkout(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    order = Order.objects.create(
        product=product,
        amount=product.price,
        status="pending",
    )

    return render(request, "payments/checkout.html", {
        "product": product,
        "order": order,
    })


def success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = "success"
    order.save()
    return render(request, "payments/success.html", {"order": order})

def cancel(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = "cancel"
    order.save()
    return render(request, "payments/cancel.html", {"order": order})


# --------------------
# 2) セットまとめ買い（DB変更なし：商品ごとにOrderを作る）
# --------------------
def checkout_set(request, set_slug):
    set_obj = get_object_or_404(Set, slug=set_slug, is_active=True)
    products = list(set_obj.products.all())

    orders = []
    total = 0

    for p in products:
        o = Order.objects.create(
            product=p,
            amount=p.price,
            status="pending",
        )
        orders.append(o)
        total += p.price

    # 成功/失敗を「セットで一括」できるように、注文IDをセッションに保存
    request.session[SESSION_KEY_SET_ORDER_IDS] = [o.id for o in orders]

    return render(request, "payments/checkout_set.html", {
        "set": set_obj,
        "products": products,
        "orders": orders,
        "total": total,
    })


def success_set(request):
    ids = request.session.get(SESSION_KEY_SET_ORDER_IDS, [])
    Order.objects.filter(id__in=ids).update(status="success")
    orders = Order.objects.filter(id__in=ids).select_related("product")
    total = sum(o.amount for o in orders)

    # 1回処理したら消す（事故防止）
    request.session.pop(SESSION_KEY_SET_ORDER_IDS, None)

    return render(request, "payments/success_set.html", {
        "orders": orders,
        "total": total,
    })


def cancel_set(request):
    ids = request.session.get(SESSION_KEY_SET_ORDER_IDS, [])
    Order.objects.filter(id__in=ids).update(status="cancel")
    orders = Order.objects.filter(id__in=ids).select_related("product")
    total = sum(o.amount for o in orders)

    request.session.pop(SESSION_KEY_SET_ORDER_IDS, None)

    return render(request, "payments/cancel_set.html", {
        "orders": orders,
        "total": total,
    })
