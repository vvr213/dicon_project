from django.contrib import admin
from .models import Street, Shop, Product

# Register your models here.

#管理画面の一覧は、デフォルトでは __str__ の戻り値しか表示しないので、一覧には 「トマト」だけ が出る。
#admin.site.register(Product)

#一覧画面に商品名｜価格が並ぶ
@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "street")
    list_filter = ("street",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "price")
    list_filter = ("shop", "shop__street")
    search_fields = ("name",)