from django.urls import path
from . import views

app_name = "dicon_app"

urlpatterns = [
    # 🏠 ホーム
    path("", views.home, name="home"),

    # 🏪 店舗 (shops)
    path("shops/", views.shop_list, name="shop_list"),
    path("shops/<int:shop_pk>/", views.shop_detail, name="shop_detail"),
    path("vacant-store/", views.vacant_store, name="vacant_store"),

    # 📦 商品 (products)
    path("products/", views.product_list, name="product_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/<int:product_pk>/consult/", views.consult_from_product, name="consult_from_product"),

    # 🧺 セット (これを消すとメニューのリンクが死にます)
    path("sets/", views.set_list, name="set_list"),
    path("set/<int:pk>/", views.set_detail, name="set_detail"),

    # urls.py の適当な場所（セットの下あたり）に追加
    path("profile/", views.profile, name="profile"),

    # 🏷️ 特売・イベント
    path("sale/", views.sale_list, name="sale_list"),
    path("events/", views.event_list, name="event_list"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),

    # 🤝 相談・コンシェルジュ
    path("consult/", views.consult_home, name="consult_home"),
    path("consult/shops/<int:shop_pk>/", views.shop_consult, name="shop_consult"),
    path("consult-menu/", views.consult_menu, name="consult_menu"),
    path("consult/chat/demo/", views.chat_demo, name="chat_demo"),
    path("concierge/", views.concierge_list, name="concierge_list"),

    # 👥 認定パートナー・ユーザー
    path("partners/", views.partner_list, name="partner_list"),
    path("profile/", views.profile, name="profile"),
    path("qa/", views.qa, name="qa"),

    # 🛒 カート・決済
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/done/", views.checkout_done, name="checkout_done"),

    # 📍 その他
    path("locker-guide/", views.locker_guide, name="locker_guide"),
]