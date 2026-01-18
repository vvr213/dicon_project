from django.contrib import admin
from .models import Street, Shop, Product, Set, HeroSlide, Event


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    # 通りマスタ
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    # 店舗マスタ
    list_display = ("id", "name", "street", "line_url")
    list_filter = ("street",)
    search_fields = ("name",)
    autocomplete_fields = ("street",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 商品（特売含む）
    list_display = ("name", "price", "shop", "is_sale", "sale_price")
    list_filter = ("is_sale", "shop__street")
    search_fields = ("name",)
    autocomplete_fields = ("shop",)


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    # おすすめセット（献立）
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("products",)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    # トップページ告知スライド
    list_display = ("order", "title", "is_active", "link_url")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("order",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    イベント管理画面

    ・季節イベント（開始日あり）
    ・定番イベント（開始日なし、schedule_textで表現）

    の両立を前提にした構成
    """

    # 一覧画面（何のイベントかを一瞬で判断できる並び）
    list_display = (
        "title",
        "category",
        "is_regular",
        "schedule_text",
        "announce_from",
        "announce_until",
        "start_date",
        "end_date",
        "is_featured",
        "is_active",
    )

    # 左側フィルタ
    list_filter = (
        "category",
        "is_regular",
        "is_featured",
        "is_active",
    )

    # 検索対象
    search_fields = (
        "title",
        "summary",
        "body",
        "location",
        "schedule_text",
    )

    # スラッグ自動生成
    prepopulated_fields = {"slug": ("title",)}

    # 編集画面の表示順
    fields = (
        "title",
        "slug",
        "category",

        "is_regular",
        "schedule_text",

        "announce_from",
        "announce_until",

        "start_date",
        "end_date",

        "summary",
        "body",

        "location",
        "map_url",
        "apply_url",

        "image",
        "share_text",

        "is_featured",
        "is_active",
    )

    # 管理画面の並び順（新しいものが上）
    ordering = ("-created_at",)
