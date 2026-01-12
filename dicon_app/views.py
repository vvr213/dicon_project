from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Product, Street, Shop, Set, HeroSlide, Event


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
        "line_url": getattr(shop, "line_url", ""),
    })


# --------------------
# トップページ
# --------------------
def home(request):
    slides = HeroSlide.objects.filter(is_active=True).order_by("order")
    sets = Set.objects.filter(is_active=True).order_by("-created_at")[:6]
    sale_products = Product.objects.filter(is_sale=True).order_by("-id")[:6]
    streets = Street.objects.all().order_by("name")[:3]
    products = Product.objects.all().order_by("-id")[:6]

    notices = [
        {"title": "時短：おすすめセットで10分ごはん", "url": reverse("dicon_app:set_list")},
        {"title": "商店街体験：通りからお店へ", "url": reverse("dicon_app:street_list")},
        {"title": "本日の特売：お得な商品をチェック", "url": reverse("dicon_app:sale_list")},
    ]

    # ✅ ここが「最重要」：home にイベント2種類を足す
    today = timezone.localdate()

    # 未来だけ見せたい（おすすめ）
    featured_events = Event.objects.filter(
        is_active=True,
        is_featured=True,
        start_date__gte=today
    ).order_by("start_date")[:5]

    upcoming_events = Event.objects.filter(
        is_active=True,
        start_date__gte=today
    ).order_by("start_date")[:12]

    # 過去も混ぜたいなら：↑の start_date__gte を消すだけでOK

    context = {
        "slides": slides,
        "sets": sets,
        "sale_products": sale_products,
        "streets": streets,
        "products": products,
        "notices": notices,
        "crumbs": [],

        # ✅ これを追加するだけ
        "featured_events": featured_events,
        "upcoming_events": upcoming_events,
        "today": today,
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
    return render(request, "dicon_app/street_list.html", {"streets": streets, "crumbs": []})


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
# おすすめセット
# --------------------
def set_list(request):
    sets = Set.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "dicon_app/set_list.html", {"sets": sets, "crumbs": [{"label": "おすすめセット", "url": None}]})


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
    return render(request, "dicon_app/sale_list.html", {"products": products, "crumbs": [{"label": "特売情報", "url": None}]})


def consult_home(request):
    presets = [
        {"key": "sashimi", "title": "刺身盛り、予算で作れます", "desc": "人数 / 予算 / 苦手食材を入れて相談", "image": "img/consult/sashimi.jpg"},
        {"key": "bbq", "title": "BBQ用に、肉と野菜まとめて", "desc": "人数 / 予算 / 焼き方（厚切り等）", "image": "img/consult/bbq.jpg"},
        {"key": "prep", "title": "下ごしらえだけお願いしたい", "desc": "ささがき / あく抜き / カット", "image": "img/consult/prep.jpg"},
        {"key": "okazu", "title": "今夜のおかず、相談して決める", "desc": "好み / 予算 / 作り置きもOK", "image": "img/consult/okazu.jpg"},
        {"key": "smoothie", "title": "スムージー用にセットしてほしい", "desc": "甘さ / アレルギー / 量", "image": "img/consult/smoothie.jpg"},
    ]
    return render(request, "dicon_app/consult_home.html", {"presets": presets})


# --------------------
# イベント
# --------------------
def event_list(request):
    today = timezone.localdate()
    events = Event.objects.filter(is_active=True, start_date__gte=today).order_by("start_date")
    return render(request, "dicon_app/event_list.html", {"events": events, "today": today})


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    share_url = request.build_absolute_uri(event.get_absolute_url())
    return render(request, "dicon_app/event_detail.html", {"event": event, "share_url": share_url})