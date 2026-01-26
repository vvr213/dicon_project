from django.urls import path
from . import views

app_name = "dicon_app"

urlpatterns = [
    path("", views.home, name="home"),

    # 店
    path("shops/<int:shop_pk>/", views.shop_detail, name="shop_detail"),
    path("shops/", views.shop_list, name="shop_list"),

    # 商品
    path("products/", views.product_list, name="product_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/<int:product_pk>/consult/", views.consult_from_product, name="consult_from_product"),

    # セット
    path("sets/", views.set_list, name="set_list"),
    path("sets/<slug:slug>/", views.set_detail, name="set_detail"),

    # 特売
    path("sale/", views.sale_list, name="sale_list"),

    # 相談
    path("consult/", views.consult_home, name="consult_home"),
    path("consult/shops/<int:shop_pk>/", views.shop_consult, name="shop_consult"),

    # イベント
    path("events/", views.event_list, name="event_list"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),

    # ロッカーガイド
    path('locker-guide/', views.locker_guide, name='locker_guide'),

    # 認定パートナー一覧ページ
    path('partners/', views.partner_list, name='partner_list'),

    path('vacant-store/', views.vacant_store, name='vacant_store'),

    path('consult/', views.consult_home, name='consult_home'),

    path('consult-menu/', views.consult_menu, name='consult_menu'),

    # マイページ
    path('profile/', views.profile, name='profile'),

    # === 🛒 お買い物機能 ===
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'), # カートに入れる
    path('cart/', views.cart_detail, name='cart_detail'),   
    # ▼▼▼ これを追加！ ▼▼▼
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # ▲▲▲ ここまで ▲▲▲                    # カートを見る
    path('checkout/', views.checkout, name='checkout'),                         # レジに進む
    path('checkout/done/', views.checkout_done, name='checkout_done'),          # 注文完了（QR表示）

    # チャットデモ用
    path('consult/chat/demo/', views.chat_demo, name='chat_demo'),

    path('qa/', views.qa, name='qa'),

    path('partner/', views.partner_list, name='partner_list'),

    path('vacant_store/', views.vacant_store, name='vacant_store'),

    path('set/<int:pk>/', views.set_detail, name='set_detail'),

    path('concierge/', views.concierge_list, name='concierge_list'),

]
