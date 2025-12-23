from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="order_list"),
]
#"" → /orders/ に対応
#views.order_list → 注文一覧画面