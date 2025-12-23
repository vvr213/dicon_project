from django.contrib import admin
from .models import Product

# Register your models here.

#管理画面の一覧は、デフォルトでは __str__ の戻り値しか表示しないので、一覧には 「トマト」だけ が出る。
#admin.site.register(Product)

#一覧画面に商品名｜価格が並ぶ
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
