from django.shortcuts import render
from .models import Order

# Create your views here.

def order_list(request):
    orders = Order.objects.select_related("product").order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})
#select_related("product")：外部キーの商品も一緒に取り、表示が速い
#order_by("-created_at")：新しい注文が上に来る
