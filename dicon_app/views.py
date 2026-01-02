from django.shortcuts import render, get_object_or_404, render
from django.urls import reverse

from .models import Product, Street, Shop, Set, HeroSlide

# 1/1追加→さらに変更
def shop_consult(request, shop_pk):
    shop = get_object_or_404(Shop.objects.select_related("street"), pk=shop_pk)

    product = request.GET.get("product", "")
    qty = request.GET.get("qty", "")
    set_name = request.GET.get("set", "")
    order_id = request.GET.get("order", "")

    lines = []
    lines.append(f"【相談】{shop.name} さんへ")
    lines.append("")
    if product:
        lines.append(f"商品：{product}")
        if qty:
            lines.append(f"数量：{qty}")
        lines.append("")
    if set_name:
        lines.append(f"セット：{set_name}")
        lines.append("")
    if order_id:
        lines.append(f"注文番号：{order_id}")
        lines.append("（この注文について相談です）")
        lines.append("")

    lines += ["希望：", "受取希望日時：", "その他："]
    draft = "\n".join(lines)

    return render(request, "dicon_app/shop_consult.html", {
        "shop": shop,
        "draft": draft,
        "line_url": shop.line_url,  # ←テンプレで使うなら渡す
    })


# --------------------
# トップページ（主役：おすすめセット）
# --------------------
def home(request):
    slides = HeroSlide.objects.filter(is_active=True).order_by("order")
    sets = Set.objects.filter(is_active=True).order_by("-created_at")[:6]
    sale_products = Product.objects.filter(is_sale=True).order_by("-id")[:6]
    streets = Street.objects.all().order_by("name")[:3]
    products = Product.objects.all().order_by("-id")[:6]

    # ✅ 「notices」はファイルではなく、このリストをテンプレに渡すだけ
    notices = [
        {"title": "① 時短：おすすめセットで10分ごはん", "url": reverse("dicon_app:set_list")},
        {"title": "② 商店街体験：通りからお店へ", "url": reverse("dicon_app:street_list")},
        {"title": "③ 本日の特売：お得な商品をチェック", "url": reverse("dicon_app:sale_list")},
    ]

    context = {
        "slides": slides,
        "sets": sets,
        "sale_products": sale_products,
        "streets": streets,
        "products": products,
        "notices": notices,  # ✅ これがないと home.html のお知らせが出ない
        "crumbs": [],
        # HeroSlide のカルーセルだけで運用する」なら、notices 自体を消す方が混乱が減る。
        # （どっちで運用するかだけ決める必要）
    }
    return render(request, "dicon_app/home.html", context)


# --------------------
# 商品一覧・詳細
# --------------------
def product_list(request):
    products = Product.objects.select_related("shop", "shop__street").all()
    return render(request, "dicon_app/product_list.html", {
        "products": products,
        "crumbs": [{"label": "商品一覧", "url": None}],
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
# 通り→店舗→商品
# --------------------
def street_list(request):
    streets = Street.objects.all().order_by("name")
    return render(request, "dicon_app/street_list.html", {
        "streets": streets,
        "crumbs": [],  # 入口なので無しでもOK
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
# おすすめセット（主役）
# --------------------
def set_list(request):
    sets = Set.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "dicon_app/set_list.html", {
        "sets": sets,
        "crumbs": [{"label": "おすすめセット", "url": None}],
    })


def set_detail(request, slug):
    set_obj = get_object_or_404(Set, slug=slug, is_active=True)
    return render(request, "dicon_app/set_detail.html", {
        "set": set_obj,
        "crumbs": [
            {"label": "おすすめセット", "url": reverse("dicon_app:set_list")},
            {"label": set_obj.name, "url": None},
        ],
    })


# --------------------
# 特売
# --------------------
def sale_list(request):
    products = Product.objects.filter(is_sale=True).order_by("-id")
    return render(request, "dicon_app/sale_list.html", {
        "products": products,
        "crumbs": [{"label": "特売情報", "url": None}],
    })


from django.shortcuts import render

def consult_home(request):
    presets = [
        {
            "key": "sashimi",
            "title": "刺身盛り、予算で作れます",
            "desc": "人数 / 予算 / 苦手食材を入れて相談",
            "image": "img/consult/sashimi.jpg",
        },
        {
            "key": "bbq",
            "title": "BBQ用に、肉と野菜まとめて",
            "desc": "人数 / 予算 / 焼き方（厚切り等）",
            "image": "img/consult/bbq.jpg",
        },
        {
            "key": "prep",
            "title": "下ごしらえだけお願いしたい",
            "desc": "ささがき / あく抜き / カット",
            "image": "img/consult/prep.jpg",
        },
        {
            "key": "okazu",
            "title": "焼いておいてほしい、作っておいてほしい",
            "desc": "塩焼き / 煮物 / 揚げ物",
            "image": "img/consult/okazu.jpg",
        },
        {
            "key": "smoothie",
            "title": "スムージー用にセットしてほしい",
            "desc": "甘さ / アレルギー / 量",
            "image": "img/consult/smoothie.jpg",
        },
    ]
    return render(request, "dicon_app/consult_home.html", {"presets": presets})
    # 画像は後で置く、今は仮でページ動かす