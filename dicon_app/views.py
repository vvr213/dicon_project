from typing import Optional, Dict
from urllib.parse import urlencode

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .models import Product, Street, Shop, Set, HeroSlide, Event


# --------------------
# 共通：preset 付きURL生成（迷子防止）
# --------------------
def _with_preset(url: str, preset: str) -> str:
    preset = (preset or "").strip()
    if not preset:
        return url
    join = "&" if "?" in url else "?"
    return f"{url}{join}{urlencode({'preset': preset})}"


# --------------------
# パンくず 1要素
# --------------------
def bc(label: str, url: Optional[str] = None) -> Dict[str, Optional[str]]:
    return {"label": label, "url": url}


# --------------------
# 相談プリセット → 店（決め打ち）
# --------------------
PRESET_TO_SHOP_NAME = {
    "sashimi": "なにわ鮮魚店",   # 刺身・盛り
    "bbq": "精肉のタナカ",        # BBQ
    "sasagaki": "八百屋山田",     # ささがき（中央通りの八百屋）
    "prep": "八百屋山田",         # 下ごしらえ系も八百屋山田に寄せるなら
    "okazu": "惣菜の近藤",         # 今夜のおかず（東商店街）
    "smoothie": "昭和青果",       # スムージー（西レトロ）
}


def _shop_pk_for_preset(preset_key: str) -> Optional[int]:
    preset_key = (preset_key or "").strip()
    shop_name = PRESET_TO_SHOP_NAME.get(preset_key)
    if not shop_name:
        return None
    shop = Shop.objects.filter(name=shop_name).first()
    return shop.pk if shop else None


# --------------------
# consult_home を「必ず一覧表示」させたい時のURL生成
# 例）相談（店）→ 相談プリセットへ戻る：/consult/?show=1&preset=sashimi
# --------------------
def _consult_home_url(preset_key: str = "") -> str:
    base = reverse("dicon_app:consult_home")
    preset_key = (preset_key or "").strip()
    if preset_key:
        return f"{base}?{urlencode({'show': '1', 'preset': preset_key})}"
    return f"{base}?show=1"


# --------------------
# 相談文生成（商店街の技が伝わる構造）
# --------------------
def _build_consult_draft(
    shop,
    preset_key="",
    product="",
    qty="",
    set_name="",
    order_id="",
    free_note="",
):
    presets_map = {
        "sashimi": {
            "title": "刺身盛り（予算で作る）",
            "skills": ["旬の目利き", "人数と予算で組む", "苦手食材の調整", "見映えの段取り"],
            "ask": ["人数", "予算", "苦手（魚）", "子ども向け/大人向け", "盛り付けの希望"],
        },
        "bbq": {
            "title": "BBQ（肉と野菜まとめて）",
            "skills": ["部位のバランス", "焼きやすい厚さ", "野菜の焼き向きカット", "タレ/味付け提案"],
            "ask": ["人数", "予算", "厚切り/薄切り", "海鮮の有無", "子ども向け/大人向け"],
        },
        "sasagaki": {
            "title": "ささがき（必要な分だけ）",
            "skills": ["ささがき", "下処理", "用途に合わせた厚み", "時短段取り"],
            "ask": ["用途（きんぴら/汁物/煮物）", "量", "太さ（細め/普通）", "受取時間"],
        },
        "prep": {
            "title": "カレーの材料（下ごしらえだけ）",
            "skills": [
        "野菜の皮むき・カット","肉のひと口カット（希望で）","炒め順まで段取り","当日すぐ作れる状態に","時短段取り",],
        "ask": ["人数（何人分）","じゃがいも：乱切り/小さめ","にんじん：厚め/薄め/❤️ハート型何個要る？",
        "玉ねぎ：くし形/薄切り","肉あり/なし（種類も）","辛さ（甘口/中辛/辛口）","受取時間",],
        },
        "okazu": {
            "title": "今夜のおかず（相談して決める）",
            "skills": ["献立提案", "予算内で組む", "作り置き対応", "味の方向性合わせ"],
            "ask": ["人数", "予算", "好み（和/洋/中）", "苦手", "作り置きの有無"],
        },
        "smoothie": {
            "title": "スムージー（果物と野菜セット）",
            "skills": ["甘さの調整", "アレルギー配慮", "比率の提案", "洗い/カット段取り"],
            "ask": ["甘さ", "アレルギー", "量（何杯分）", "入れたくない食材", "色味の希望"],
        },
    }

    p = presets_map.get((preset_key or "").strip())

    lines = []
    lines.append(f"【相談】{shop.name} さんへ")
    lines.append("")
    lines.append("いつもありがとうございます。迷うところだけ相談させてください。")
    lines.append("")

    if p:
        lines.append(f"■相談の種類：{p['title']}")
        lines.append("■お願いしたいこと（技）：" + " / ".join(p["skills"]))
        lines.append("")

    if product:
        lines.append(f"■商品：{product}")
    if qty:
        lines.append(f"■数量：{qty}")
    if set_name:
        lines.append(f"■セット：{set_name}")
    if order_id:
        lines.append(f"■注文番号：{order_id}")
    if product or qty or set_name or order_id:
        lines.append("")

    lines.append("■人数：")
    lines.append("■予算：")
    lines.append("■苦手・アレルギー：")
    lines.append("")

    if p:
        lines.append("■お店に伝えるポイント（分かる範囲でOK）")
        for item in p["ask"]:
            lines.append(f"・{item}：")
        lines.append("")

    lines.append("■受け取り希望")
    lines.append("・希望日時：")
    lines.append("・時間の幅（例 18:00〜18:30）：")
    lines.append("")

    lines.append("■備考（任意）")
    lines.append("・子ども向け／大人向け：")
    lines.append("・味の方向（薄味/しっかり/辛さなし等）：")
    if free_note:
        lines.append(f"・追記：{free_note}")

    return "\n".join(lines)


# --------------------
# トップページ
# --------------------
def home(request):
    preset_key = (request.GET.get("preset") or "").strip()
    if preset_key:
        shop_pk = _shop_pk_for_preset(preset_key)
        if shop_pk:
            return redirect(
                _with_preset(
                    reverse("dicon_app:shop_consult", kwargs={"shop_pk": shop_pk}),
                    preset_key,
                )
            )

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

    today = timezone.localdate()
    base_qs = Event.objects.filter(is_active=True)

    regular_events = base_qs.filter(is_regular=True).filter(
        Q(announce_from__isnull=True) | Q(announce_from__lte=today)
    ).filter(
        Q(announce_until__isnull=True) | Q(announce_until__gte=today)
    ).order_by("-is_featured", "category", "title")

    spot_upcoming = base_qs.filter(is_regular=False).filter(
        Q(end_date__gte=today) | Q(end_date__isnull=True, start_date__gte=today)
    ).order_by("start_date", "-created_at")

    season_event = spot_upcoming.filter(category="season").first()

    event_carousel_items = []
    if season_event:
        event_carousel_items.append(season_event)
    event_carousel_items += list(regular_events[:10])

    upcoming_events = spot_upcoming[:12]

    context = {
        "slides": slides,
        "sets": sets,
        "sale_products": sale_products,
        "streets": streets,
        "products": products,
        "notices": notices,
        "crumbs": [],
        "today": today,
        "event_carousel_items": event_carousel_items,
        "upcoming_events": upcoming_events,
    }
    return render(request, "dicon_app/home.html", context)


# --------------------
# 相談：プリセット入口
# --------------------
def consult_home(request):
    preset_key = (request.GET.get("preset") or "").strip()
    show = (request.GET.get("show") or "").strip() == "1"

    # show=1 のときは「一覧表示」優先で redirect しない
    if preset_key and not show:
        shop_pk = _shop_pk_for_preset(preset_key)
        if shop_pk:
            return redirect(
                _with_preset(
                    reverse("dicon_app:shop_consult", kwargs={"shop_pk": shop_pk}),
                    preset_key,
                )
            )

    presets = [
        {
            "key": "sashimi",
            "title": "刺身盛り、予算で作れます",
            "desc": "人数・予算・苦手を言うだけ。旬の魚を組み合わせて、見映えまで段取りします。",
            "image": "img/consult/sashimi.jpg",
            "skills": ["旬の目利き", "盛りの段取り", "苦手調整", "予算内で組む"],
            "ask": ["人数", "予算", "苦手（魚）", "子ども/大人", "盛りの希望"],
            "shop_pk": _shop_pk_for_preset("sashimi"),
        },
        {
            "key": "bbq",
            "title": "BBQ用に、肉と野菜まとめて",
            "desc": "焼きやすい厚さに切って、部位もバランスよく。野菜は焼き向きにカットします。",
            "image": "img/consult/bbq.jpg",
            "skills": ["部位バランス", "焼きやすい厚さ", "野菜カット", "味付け提案"],
            "ask": ["人数", "予算", "厚切り/薄切り", "海鮮の有無", "子ども向け"],
            "shop_pk": _shop_pk_for_preset("bbq"),
        },
        {
            "key": "sasagaki",
            "title": "ささがき、必要な分だけ",
            "desc": "用途と量を言うだけ。太さも合わせて、すぐ使える状態にして渡します。",
            "image": "img/consult/prep.jpg",
            "skills": ["ささがき", "下処理", "厚み調整", "時短段取り"],
            "ask": ["用途", "量", "太さ", "受取時間"],
            "shop_pk": _shop_pk_for_preset("sasagaki"),
        },
        {
            "key": "prep",
            "title": "カレーの材料にしてほしい",
            "desc": "じゃがいも・にんじん・玉ねぎを、家で切らんでOKな状態に。帰ったら炒めて煮るだけにします。",
            "image": "img/consult/curry_prep.png",
            "skills": ["皮むき", "カット指定", "厚み調整", "当日すぐ調理", "時短段取り"],
            "ask": ["人数（何人分）", "切り方（じゃが/にんじん/玉ねぎ）", "肉あり/なし", "辛さ", "受取時間"],
            "shop_pk": _shop_pk_for_preset("prep"),
        },
        {
            "key": "okazu",
            "title": "今夜のおかず、相談して決める",
            "desc": "好みと予算で、今日の献立を一緒に決めます。作り置き向きにも組み替えOK。",
            "image": "img/consult/okazu.jpg",
            "skills": ["献立提案", "予算内", "作り置き対応", "味合わせ"],
            "ask": ["人数", "予算", "好み（和/洋/中）", "苦手", "作り置きの有無"],
            "shop_pk": _shop_pk_for_preset("okazu"),
        },
        {
            "key": "smoothie",
            "title": "スムージー用にセットしてほしい",
            "desc": "甘さ・アレルギー・量を聞いて、果物と野菜を“ちょうどいい比率”でセットします。",
            "image": "img/consult/smoothie.jpg",
            "skills": ["甘さ調整", "アレルギー配慮", "比率提案", "洗い/カット"],
            "ask": ["甘さ", "アレルギー", "量（何杯分）", "入れたくない食材", "色味"],
            "shop_pk": _shop_pk_for_preset("smoothie"),
        },
    ]

    return render(
        request,
        "dicon_app/consult_home.html",
        {
            "presets": presets,
            "crumbs": [{"label": "相談プリセット", "url": None}],
        },
    )


# --------------------
# 相談：店ごとの相談（LINE下書き）
# --------------------
def shop_consult(request, shop_pk):
    preset_key = (request.GET.get("preset") or "").strip()

    shop = get_object_or_404(Shop.objects.select_related("street"), pk=shop_pk)

    product = request.GET.get("product", "")
    qty = request.GET.get("qty", "")
    set_name = request.GET.get("set", "")
    order_id = request.GET.get("order", "")
    free_note = (request.GET.get("note") or "").strip()

    draft = _build_consult_draft(
        shop=shop,
        preset_key=preset_key,
        product=product,
        qty=qty,
        set_name=set_name,
        order_id=order_id,
        free_note=free_note,
    )

    # ✅ 相談プリセット一覧へ戻る（必ず一覧表示：show=1）
    consult_home_url = _consult_home_url(preset_key)

    # ✅ お店詳細へ戻る（preset保持）
    back_to_shop_detail_url = _with_preset(
        reverse("dicon_app:shop_detail", kwargs={"shop_pk": shop.pk}),
        preset_key,
    )

    return render(
        request,
        "dicon_app/shop_consult.html",
        {
            "shop": shop,
            "draft": draft,
            "line_url": getattr(shop, "line_url", ""),
            "preset": preset_key,
            "consult_home_url": consult_home_url,
            "back_to_shop_detail_url": back_to_shop_detail_url,
            "crumbs": [
                bc("相談プリセット", url=consult_home_url),
                bc("通り一覧", url=_with_preset(reverse("dicon_app:street_list"), preset_key)),
                bc(
                    shop.street.name,
                    url=_with_preset(
                        reverse("dicon_app:shop_list_by_street", kwargs={"street_slug": shop.street.slug}),
                        preset_key,
                    ),
                ),
                bc(shop.name, url=back_to_shop_detail_url),
                bc("相談"),
            ],
        },
    )


# --------------------
# 商品一覧・詳細
# --------------------
def product_list(request):
    products = Product.objects.select_related("shop", "shop__street").all()
    return render(
        request,
        "dicon_app/product_list.html",
        {"products": products, "crumbs": [bc("商品一覧")]},
    )


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related("shop", "shop__street"), pk=pk)
    return render(
        request,
        "dicon_app/product_detail.html",
        {
            "product": product,
            "crumbs": [
                bc("商品一覧", url=reverse("dicon_app:product_list")),
                bc(product.name),
            ],
        },
    )


# --------------------
# 通り→店舗→商品（preset 引き継ぎ＋パンくず）
# --------------------
def street_list(request):
    preset = (request.GET.get("preset") or "").strip()
    streets = Street.objects.all().order_by("name")
    return render(
        request,
        "dicon_app/street_list.html",
        {"streets": streets, "preset": preset, "crumbs": [bc("通り一覧")]},
    )


def shop_list_by_street(request, street_slug):
    preset = (request.GET.get("preset") or "").strip()
    street = get_object_or_404(Street, slug=street_slug)
    shops = Shop.objects.filter(street=street).order_by("name")
    return render(
        request,
        "dicon_app/shop_list.html",
        {
            "street": street,
            "shops": shops,
            "preset": preset,
            "crumbs": [
                bc("通り一覧", url=_with_preset(reverse("dicon_app:street_list"), preset)),
                bc(street.name),
            ],
        },
    )


def shop_detail(request, shop_pk):
    preset = (request.GET.get("preset") or "").strip()

    shop = get_object_or_404(Shop.objects.select_related("street"), pk=shop_pk)
    products = Product.objects.filter(shop=shop).order_by("name")

    street_list_url = _with_preset(reverse("dicon_app:street_list"), preset)
    shop_list_url = _with_preset(
        reverse("dicon_app:shop_list_by_street", kwargs={"street_slug": shop.street.slug}),
        preset,
    )
    consult_url = _with_preset(
        reverse("dicon_app:shop_consult", kwargs={"shop_pk": shop.pk}),
        preset,
    )

    return render(
        request,
        "dicon_app/shop_detail.html",
        {
            "shop": shop,
            "products": products,
            "preset": preset,
            "consult_url": consult_url,
            "crumbs": [
                bc("通り一覧", url=street_list_url),
                bc(shop.street.name, url=shop_list_url),
                bc(shop.name),
            ],
        },
    )


# --------------------
# おすすめセット
# --------------------
def set_list(request):
    sets = Set.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "dicon_app/set_list.html", {"sets": sets, "crumbs": [bc("おすすめセット")]})


def set_detail(request, slug):
    set_obj = get_object_or_404(Set, slug=slug, is_active=True)
    return render(
        request,
        "dicon_app/set_detail.html",
        {"set": set_obj, "crumbs": [bc("おすすめセット", url=reverse("dicon_app:set_list")), bc(set_obj.name)]},
    )


# --------------------
# 特売
# --------------------
def sale_list(request):
    products = Product.objects.filter(is_sale=True).order_by("-id")
    return render(request, "dicon_app/sale_list.html", {"products": products, "crumbs": [bc("特売情報")]})


# --------------------
# イベント
# --------------------
def event_list(request):
    today = timezone.localdate()
    tag = (request.GET.get("tag") or "").strip()
    q = (request.GET.get("q") or "").strip()

    base_qs = Event.objects.filter(is_active=True)

    regular_events = base_qs.filter(is_regular=True).filter(
        Q(announce_from__isnull=True) | Q(announce_from__lte=today)
    ).filter(
        Q(announce_until__isnull=True) | Q(announce_until__gte=today)
    )

    events = base_qs.filter(is_regular=False).filter(
        Q(end_date__gte=today) | Q(end_date__isnull=True, start_date__gte=today)
    )

    if tag:
        regular_events = regular_events.filter(category=tag)
        events = events.filter(category=tag)

    if q:
        cond = (
            Q(title__icontains=q)
            | Q(summary__icontains=q)
            | Q(body__icontains=q)
            | Q(location__icontains=q)
            | Q(schedule_text__icontains=q)
        )
        regular_events = regular_events.filter(cond)
        events = events.filter(cond)

    regular_events = regular_events.order_by("-is_featured", "category", "title")
    events = events.order_by("start_date", "-is_featured")

    context = {
        "today": today,
        "tag": tag,
        "q": q,
        "regular_events": regular_events,
        "events": events,
        "category_choices": Event.CATEGORY_CHOICES,
        "crumbs": [bc("イベント")],
    }
    return render(request, "dicon_app/event_list.html", context)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    share_url = request.build_absolute_uri(event.get_absolute_url())
    return render(
        request,
        "dicon_app/event_detail.html",
        {
            "event": event,
            "share_url": share_url,
            "crumbs": [bc("イベント", url=reverse("dicon_app:event_list")), bc(event.title)],
        },
    )
