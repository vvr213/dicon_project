from django.urls import path
from . import views

app_name = "dicon_app"

urlpatterns = [
    path("", views.home, name="home"),

    # products
    path("products/", views.product_list, name="product_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),

    # streets / shops
    path("streets/", views.street_list, name="street_list"),
    path("streets/<slug:street_slug>/shops/", views.shop_list_by_street, name="shop_list_by_street"),
    path("shops/<int:shop_pk>/", views.shop_detail, name="shop_detail"),

    # sets
    path("sets/", views.set_list, name="set_list"),
    path("sets/<slug:slug>/", views.set_detail, name="set_detail"),

    # sale
    path("sale/", views.sale_list, name="sale_list"),

    # consult
    path("consult/", views.consult_home, name="consult_home"),
    path("shops/<int:shop_pk>/consult/", views.shop_consult, name="shop_consult"),

    # events
    path("events/", views.event_list, name="event_list"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
]
