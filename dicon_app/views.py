from django.shortcuts import render, get_object_or_404
from .models import Street, Shop, Product

# Create your views here.
#商品一覧
def product_list(request):
    products = Product.objects.select_related("shop", "shop__street").all()
    return render(request, "dicon_app/product_list.html", {"products": products})
#③ ブラウザにレスポンスとして返す   ① どのHTMLを使うか決めている       ② どのデータを使うか決めている
#商品詳細
def product_detail(request, pk):  # ← 追加12/24
    product = get_object_or_404(Product.objects.select_related("shop__street"), pk=pk)
    return render(request, "dicon_app/product_detail.html", {"product": product})

#通り一覧
def street_list(request):
    streets = Street.objects.all().order_by("name")
    return render(request, "dicon_app/street_list.html", 
    {"streets": streets,
    "crumbs": [],
    })

#通り → 店舗一覧
def shop_list_by_street(request, street_slug):
    street = get_object_or_404(Street, slug=street_slug)
    shops = Shop.objects.filter(street=street).order_by("name")
    return render(request, "dicon_app/shop_list.html", {
        "street": street,
        "shops": shops,
        "crumbs": [
            {"label": street.name, "url": None},
        ],
    })

#店舗 → 商品一覧
def shop_detail(request, shop_pk):
    shop = get_object_or_404(Shop, pk=shop_pk)
    products = Product.objects.filter(shop=shop).order_by("name")
    return render(request, "dicon_app/shop_detail.html", {
        "shop": shop,
        "products": products,
        "crumbs": [
            {"label": shop.street.name, "url": f"/streets/{shop.street.slug}/"},
            {"label": shop.name, "url": None},
        ],
    })