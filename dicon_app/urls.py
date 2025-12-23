from django.urls import path
from . import views

app_name = "dicon_app"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
]
#これで「/products/」にアクセスしたら一覧が出る“入口”ができた。