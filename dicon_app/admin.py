from django.contrib import admin
from .models import Street, Shop, Product, Event, HeroSlide, Set, HomePickup, Partner, ConsultationItem

# 通り（Street）の管理設定
@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')

# 店舗（Shop）の管理設定
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    # 🆕 ここに 'category' を追加！
    list_display = ('name', 'category', 'street', 'latitude', 'longitude')
    # 🆕 ここにも 'category' を追加！
    fields = ('category', 'name', 'street', 'description', 'image', 'line_url', 'latitude', 'longitude')
    # 🆕 右側のフィルターにも追加！
    list_filter = ('category', 'street')

# 商品（Product）の管理設定
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'shop', 'is_sale')
    fields = ('category', 'name', 'price', 'shop', 'image', 'is_sale', 'sale_price')
    list_filter = ('category', 'shop', 'is_sale')
    search_fields = ('name', 'category')

# イベント（Event）の管理設定
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'body')

# トップ画像スライド（HeroSlide）の管理設定
@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')

# セット（Set）の管理設定
@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    # 一覧画面で見える項目（名前、価格、表示状態）
    list_display = ('name', 'price', 'is_active')
    
    # 編集画面で入力する項目（ここに 'image' を入れることで入力欄が出ます！）
    fields = ('name', 'slug', 'image', 'price', 'description', 'products', 'is_active')

@admin.register(HomePickup)
class HomePickupAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_text', 'order', 'is_active')
    list_editable = ('order', 'is_active') # 一覧画面で直接編集可能にする
    ordering = ('order',)

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')

# 一番上の import に ConsultationItem を追加
@admin.register(ConsultationItem)
class ConsultationItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'preset_id', 'color_theme', 'order', 'is_active')
    list_editable = ('order', 'is_active')