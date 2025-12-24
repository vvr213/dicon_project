from django.shortcuts import render, get_object_or_404
from .models import Product, Street, Shop, Set, HeroSlide   #追加12/24

# Create your views here.

#商品一覧
# def product_list(request):
#     products = Product.objects.select_related("shop", "shop__street").all()
#     return render(request, "dicon_app/product_list.html", {"products": products})
# #③ ブラウザにレスポンスとして返す   ① どのHTMLを使うか決めている       ② どのデータを使うか決めている
# #商品詳細
# def product_detail(request, pk):  # ← 追加12/24
#     product = get_object_or_404(Product.objects.select_related("shop__street"), pk=pk)
#     return render(request, "dicon_app/product_detail.html", {"product": product})

# #通り一覧
# def street_list(request):
#     streets = Street.objects.all().order_by("name")
#     return render(request, "dicon_app/street_list.html", 
#     {"streets": streets,
#     "crumbs": [],
#     })

# #通り → 店舗一覧
# def shop_list_by_street(request, street_slug):
#     street = get_object_or_404(Street, slug=street_slug)
#     shops = Shop.objects.filter(street=street).order_by("name")
#     return render(request, "dicon_app/shop_list.html", {
#         "street": street,
#         "shops": shops,
#         "crumbs": [
#             {"label": street.name, "url": None},
#         ],
#     })

# #店舗 → 商品一覧
# def shop_detail(request, shop_pk):
#     shop = get_object_or_404(Shop, pk=shop_pk)
#     products = Product.objects.filter(shop=shop).order_by("name")
#     return render(request, "dicon_app/shop_detail.html", {
#         "shop": shop,
#         "products": products,
#         "crumbs": [
#             {"label": shop.street.name, "url": f"/streets/{shop.street.slug}/"},
#             {"label": shop.name, "url": None},
#         ],
#     })

def home(request):
    slides = HeroSlide.objects.filter(is_active=True).order_by("order")
    sets = Set.objects.filter(is_active=True).order_by("-created_at")[:6]
    sale_products = Product.objects.filter(is_sale=True).order_by("-id")[:6]
    streets = Street.objects.all().order_by("name")[:3]
    products = Product.objects.all().order_by("-id")[:6]  # 人気っぽく見せる用（最初は新着でOK）

    context = {
        "slides": slides,
        "sets": sets,
        "sale_products": sale_products,
        "streets": streets,
        "products": products,
    }
    return render(request, "dicon_app/home.html", context)


def set_list(request):
    sets = Set.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "dicon_app/set_list.html", {"sets": sets})


def set_detail(request, slug):
    set_obj = get_object_or_404(Set, slug=slug, is_active=True)
    return render(request, "dicon_app/set_detail.html", {"set": set_obj})


def sale_list(request):
    products = Product.objects.filter(is_sale=True).order_by("-id")
    return render(request, "dicon_app/sale_list.html", {"products": products})