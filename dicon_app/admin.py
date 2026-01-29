from django.contrib import admin
from .models import (
    Street, Shop, Product, Set, Event, 
    HeroSlide, HomePickup, Partner, ConciergeItem, ConsultationItem
)

@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'street']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'price']

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

@admin.register(HomePickup)
class HomePickupAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']

@admin.register(ConciergeItem)
class ConciergeItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active'] # order を削りました

@admin.register(ConsultationItem)
class ConsultationItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']