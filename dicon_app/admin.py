from django.contrib import admin
from .models import Street, Shop, Product, Set, HeroSlide


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "street", "line_url")
    list_filter = ("street",)
    search_fields = ("name",)
    autocomplete_fields = ("street",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "shop", "is_sale", "sale_price")
    list_filter = ("is_sale", "shop__street")
    search_fields = ("name",)
    autocomplete_fields = ("shop",)


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    # filter_horizontal = ("products",)
    autocomplete_fields = ("products",)   # ← セット編集画面で商品探すのが便利


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "is_active", "link_url")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("order",)
