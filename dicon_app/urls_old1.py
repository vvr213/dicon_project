from django.urls import path
from . import views

app_name = "dicon_app"

urlpatterns = [
    path("", views.home, name="home"),  # ← 入口をhomeにする
    path("products/", views.product_list, name="product_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),

    path("streets/", views.street_list, name="street_list"),
    path("streets/<slug:street_slug>/", views.shop_list_by_street, name="shop_list_by_street"),
    path("shops/<int:shop_pk>/", views.shop_detail, name="shop_detail"),

    path("sets/", views.set_list, name="set_list"),# 追加12/24
    path("sets/<slug:slug>/", views.set_detail, name="set_detail"),# 追加12/24
    path("sale/", views.sale_list, name="sale_list"),# 追加12/24
]
