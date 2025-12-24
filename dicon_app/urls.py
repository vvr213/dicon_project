from django.urls import path
from . import views

app_name = "dicon_app"

urlpatterns = [
    path("", views.product_list, name="product_list"),  # 既存のトップ（商品一覧）にしたいなら
    path("products/<int:pk>/", views.product_detail, name="product_detail"),  # ← 追加12/24
    path("streets/", views.street_list, name="street_list"),
    path("streets/<slug:street_slug>/", views.shop_list_by_street, name="shop_list_by_street"),
    path("shops/<int:shop_pk>/", views.shop_detail, name="shop_detail"),
    path("products/", views.product_list, name="product_list"),
]
#これで「/products/」にアクセスしたら一覧が出る“入口”ができた。