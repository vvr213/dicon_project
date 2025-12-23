from django.urls import path
from . import views

app_name = "payments"
#success/cancel にも product_id
#checkout で Order を作るので、成功/失敗は product_id じゃなく order_id で受ける
urlpatterns = [
    path("checkout/<int:product_id>/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.success, name="success"),
    path("cancel/<int:order_id>/", views.cancel, name="cancel"),
]
#これで success(request, order_id) に order_id が渡る