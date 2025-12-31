from django.urls import path
from . import views

app_name = "payments"
#success/cancel にも product_id
#checkout で Order を作るので、成功/失敗は product_id じゃなく order_id で受ける
urlpatterns = [
    path("checkout/<int:product_id>/", views.checkout, name="checkout"),

    path("checkout-set/<slug:set_slug>/", views.checkout_set, name="checkout_set"),  # ←セットでカートへを追加
    path("success-set/", views.success_set, name="success_set"),  # ←追加
    path("cancel-set/", views.cancel_set, name="cancel_set"),    # ←追加

    path("success/<int:order_id>/", views.success, name="success"),
    path("cancel/<int:order_id>/", views.cancel, name="cancel"),
]
#これで success(request, order_id) に order_id が渡る