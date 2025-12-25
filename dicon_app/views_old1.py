from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Product, Street, Shop, Set, HeroSlide   #追加12/24

# Create your views here.

# --------------------
# トップページ（新）
# --------------------
def home(request):
    slides = HeroSlide.objects.filter(is_active=True).order_by("order")
    sets = Set.objects.filter(is_active=True).order_by("-created_at")[:6]
    sale_products = Product.objects.filter(is_sale=True).order_by("-id")[:6]
    streets = Street.objects.all().order_by("name")[:3]
    products = Product.objects.all().order_by("-id")[:6]  # 最初は新着でOK

    # 「お知らせカルーセル」（JSなしで確実に動く）homeに notices を追加
    notices = [
        {"title": "年末セール準備中！", "url": reverse("dicon_app:sale_list")},
        {"title": "おすすめセット更新予定", "url": reverse("dicon_app:set_list")},
        {"title": "通りからお店を探せます", "url": reverse("dicon_app:street_list")},
    ]

    context = {
        "slides": slides,
        "sets": sets,
        "sale_products": sale_products,
        "streets": streets,
        "products": products,
        "notices": notices,   # ←追加
        "crumbs": [],  # トップはパンくず無し
    }
    return render(request, "dicon_app/home.html", context)


# --------------------
# 既存（復刻）: 商品一覧・詳細
# --------------------
def product_list(request):
    products = Product.objects.select_related("shop", "shop__street").all()
    return render(request, "dicon_app/product_list.html", {
        "products": products,
        "crumbs": [],
    })


def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related("shop", "shop__street"),
        pk=pk
    )
    return render(request, "dicon_app/product_detail.html", {
        "product": product,
        "crumbs": [
            {"label": "商品一覧", "url": reverse("dicon_app:product_list")},
            {"label": product.name, "url": None},
        ],
    })


# --------------------
# 既存（復刻）: 通り→店舗→商品
# --------------------
def street_list(request):
    streets = Street.objects.all().order_by("name")
    return render(request, "dicon_app/street_list.html", {
        "streets": streets,
        "crumbs": [],
    })


def shop_list_by_street(request, street_slug):
    street = get_object_or_404(Street, slug=street_slug)
    shops = Shop.objects.filter(street=street).order_by("name")
    return render(request, "dicon_app/shop_list.html", {
        "street": street,
        "shops": shops,
        "crumbs": [
            {"label": "通り一覧", "url": reverse("dicon_app:street_list")},
            {"label": street.name, "url": None},
        ],
    })


def shop_detail(request, shop_pk):
    shop = get_object_or_404(Shop.objects.select_related("street"), pk=shop_pk)
    products = Product.objects.filter(shop=shop).order_by("name")
    return render(request, "dicon_app/shop_detail.html", {
        "shop": shop,
        "products": products,
        "crumbs": [
            {"label": "通り一覧", "url": reverse("dicon_app:street_list")},
            {"label": shop.street.name, "url": reverse("dicon_app:shop_list_by_street", kwargs={"street_slug": shop.street.slug})},
            {"label": shop.name, "url": None},
        ],
    })


# --------------------
# セット（新）
# --------------------
def set_list(request):
    sets = Set.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "dicon_app/set_list.html", {
        "sets": sets,
        "crumbs": [{"label": "セット一覧", "url": None}],
    })


def set_detail(request, slug):
    set_obj = get_object_or_404(Set, slug=slug, is_active=True)
    return render(request, "dicon_app/set_detail.html", {
        "set": set_obj,
        "crumbs": [
            {"label": "セット一覧", "url": reverse("dicon_app:set_list")},
            {"label": set_obj.name, "url": None},
        ],
    })


# --------------------
# セール（新）
# --------------------
def sale_list(request):
    products = Product.objects.filter(is_sale=True).order_by("-id")
    return render(request, "dicon_app/sale_list.html", {
        "products": products,
        "crumbs": [{"label": "特売情報", "url": None}],
    })
