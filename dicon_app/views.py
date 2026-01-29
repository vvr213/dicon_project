from typing import Optional, Dict
from urllib.parse import urlencode

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

# インポートする名前をモデル（Set）に合わせました
from .models import (
    Shop, Product, Event, HeroSlide, Street, 
    HomePickup, ConciergeItem, Partner, 
    Set, ConsultationItem
)

# ==========================================
# 1. 便利な道具（ヘルパー関数）
# ==========================================

def bc(label: str, url: Optional[str] = None) -> Dict[str, Optional[str]]:
    """パンくずリスト作成：base.htmlのcrumbsに渡すデータを作ります"""
    return {"label": label, "url": url}

def _with_preset(url: str, preset: str) -> str:
    """URLに相談プリセットパラメータを付与"""
    preset = (preset or "").strip()
    if not preset:
        return url
    join = "&" if "?" in url else "?"
    return f"{url}{join}{urlencode({'preset': preset})}"

def _get_consult_presets():
    """相談メニューのデータ定義"""
    return [
        {"key": "fish", "title": "刺身盛り、予算で作れます", "desc": "人数・予算・苦手を言うだけ...", "image": "img/consult/sashimi.jpg"},
        {"key": "bbq", "title": "BBQ用に、肉と野菜まとめて", "desc": "焼きやすい厚さに切って...", "image": "img/consult/bbq.jpg"},
        {"key": "sasagaki", "title": "ささがき、必要な分だけ", "desc": "用途と量を言うだけ。太さも合わせて...", "image": "img/consult/prep.jpg"},
        {"key": "curry", "title": "カレーの材料にしてほしい", "desc": "じゃがいも・にんじん・玉ねぎを皮むき＆カット済みで...", "image": "img/consult/curry_prep.jpg"},
        {"key": "okazu", "title": "今夜のおかず、提案して", "desc": "好みと予算を言えば、プロが提案...", "image": "img/consult/okazu.jpg"},
    ]


# ==========================================
# 2. ビュー関数（メイン機能）
# ==========================================

# --------------------
# トップページ
# --------------------
def home(request):
    """トップページ：特売、献立、イベント、告知を集めて表示"""
    slides = HeroSlide.objects.filter(is_active=True).order_by('order')
    home_pickups = HomePickup.objects.filter(is_active=True).order_by('order')[:6]
    sale_products = Product.objects.filter(is_sale=True).order_by('?')[:6]
    recommended_sets = Set.objects.filter(is_active=True).order_by('-created_at')[:3]
    concierge_items = ConciergeItem.objects.filter(is_active=True).order_by('order')[:3]
    consultation_items = ConsultationItem.objects.filter(is_active=True).order_by('order')[:3]
    today = timezone.localdate()
    upcoming_events = Event.objects.filter(is_active=True, start_date__gte=today).order_by('start_date')[:4]
    partners = Partner.objects.filter(is_active=True).order_by('order')[:4]

    return render(request, 'dicon_app/home.html', {
        'slides': slides,
        'sale_products': sale_products,
        'recommended_sets': recommended_sets,
        'upcoming_events': upcoming_events,
        'home_pickups': home_pickups,       
        'concierge_items': concierge_items,
        'consultation_items': consultation_items,
        'partners': partners,
    })

# --------------------
# セット一覧
# --------------------
def set_list(request):
    """献立セット一覧：カテゴリ絞り込み対応"""
    sets = Set.objects.filter(is_active=True).order_by("-created_at")
    category_slug = request.GET.get('category')
    if category_slug:
        sets = sets.filter(category=category_slug)

    context = {
        'sets': sets,
        'current_category': category_slug, # これからコメントアウトでフィルターとかの言葉残しとけ！
        'categories': [
            ('beauty', '美容・デトックス'), ('health', '健康維持・数値改善'),
            ('speedy', '時短・忙しい人向け'), ('diet', '糖質制限・ダイエット'),
            ('reward', '週末のご褒美'),
        ],
        'crumbs': [bc("管理栄養士の献立セット")],
    }
    return render(request, "dicon_app/set_list.html", context)

# --------------------
# セット詳細
# --------------------
def set_detail(request, pk=None, slug=None):
    """セット商品の詳細ページを表示する"""
    if pk:
        set_obj = get_object_or_404(Set, pk=pk, is_active=True)
    elif slug:
        set_obj = get_object_or_404(Set, slug=slug, is_active=True)
    else:
        return redirect('dicon_app:set_list')
        
    return render(request, "dicon_app/set_detail.html", {
        "set": set_obj,
        "crumbs": [bc("献立セット", reverse("dicon_app:set_list")), bc(set_obj.name)],
    })

# --------------------
# お店一覧
# --------------------
def shop_list(request):
    """店舗一覧＆カテゴリ絞り込み"""
    shops = Shop.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        shops = shops.filter(category=category_slug)

    return render(request, 'dicon_app/shop_list.html', {
        'shops': shops,
        'current_category': category_slug, # フィルター
        'crumbs': [bc("お店一覧")],
    })

# --------------------
# お店詳細
# --------------------
def shop_detail(request, shop_pk):
    """お店詳細：取扱商品一覧"""
    shop = get_object_or_404(Shop, pk=shop_pk)
    products = Product.objects.filter(shop=shop)
    return render(request, "dicon_app/shop_detail.html", {
        "shop": shop,
        "products": products,
        "crumbs": [bc("お店一覧", reverse("dicon_app:shop_list")), bc(shop.name)],
    })

# --------------------
# 商品一覧
# --------------------
def product_list(request):
    """商品一覧＆カテゴリ絞り込み"""
    products = Product.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category=category_slug)

    return render(request, 'dicon_app/product_list.html', {
        'products': products,
        'current_category': category_slug, # フィルター
        'crumbs': [bc("商品一覧")],
    })

# --------------------
# 商品詳細
# --------------------
def product_detail(request, pk):
    """商品詳細ページ"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "dicon_app/product_detail.html", {
        "product": product,
        "crumbs": [bc("商品一覧", reverse("dicon_app:product_list")), bc(product.name)],
    })


# ==========================
# 🛒 買い物・カート機能
# ==========================

def add_to_cart(request, product_id):
    """商品をカートに入れる"""
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('dicon_app:cart_detail')

def remove_from_cart(request, product_id):
    """カートから商品を削除"""
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('dicon_app:cart_detail')

def cart_detail(request):
    """カートの中身を表示"""
    cart = request.session.get('cart', {})
    items = []
    total_price = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = (product.sale_price if product.is_sale and product.sale_price else product.price) * quantity
            total_price += subtotal
            items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        except Product.DoesNotExist: continue
    return render(request, 'dicon_app/cart.html', {
        'items': items, 
        'total_price': total_price,
        'crumbs': [bc("買い物かご")]
    })

def checkout(request): 
    """レジ画面"""
    return render(request, 'dicon_app/checkout.html', {'crumbs': [bc("注文確認")]})

def checkout_done(request):
    """注文完了画面"""
    request.session['cart'] = {}
    return render(request, 'dicon_app/checkout_done.html', {'crumbs': [bc("注文完了")]})


# ==========================
# 💬 相談・チャット機能
# ==========================

def consult_menu(request):
    """相談メニュー一覧"""
    items = ConsultationItem.objects.filter(is_active=True).order_by('order')
    return render(request, 'dicon_app/consult_menu.html', {
        'items': items,
        'crumbs': [bc("わがまま相談")]
    })

def consult_home(request):
    """相談ホーム"""
    preset_key = request.GET.get('preset')
    item = ConsultationItem.objects.filter(preset_id=preset_key).first()
    context = {'preset_title': item.title, 'preset_desc': item.description} if item else {}
    context['crumbs'] = [bc("チャット相談")]
    return render(request, 'dicon_app/consult_chat.html', context)

def shop_consult(request, shop_pk):
    """店舗詳細から相談へ"""
    shop = get_object_or_404(Shop, pk=shop_pk)
    return render(request, 'dicon_app/consult_chat.html', {
        'preset_title': f"{shop.name}への相談",
        'crumbs': [bc("店舗相談")]
    })

def consult_from_product(request, product_pk):
    """商品詳細から相談へ"""
    product = get_object_or_404(Product, pk=product_pk)
    return redirect(f"{reverse('dicon_app:chat_demo')}?product={product.name}")

def chat_demo(request): 
    """チャットデモ"""
    return render(request, 'dicon_app/chat_demo.html')


# ==========================
# 📅 イベント・特売・その他
# ==========================

def sale_list(request):
    """特売品一覧"""
    products = Product.objects.filter(is_sale=True)
    return render(request, "dicon_app/sale_list.html", {
        "products": products,
        "crumbs": [bc("本日の特売品")]
    })

def event_list(request):
    """イベント一覧"""
    events = Event.objects.filter(is_active=True)
    return render(request, "dicon_app/event_list.html", {
        "events": events,
        "crumbs": [bc("商店街のイベント")]
    })

def event_detail(request, slug):
    """イベント詳細"""
    event = get_object_or_404(Event, slug=slug, is_active=True)
    return render(request, "dicon_app/event_detail.html", {
        "event": event,
        "crumbs": [bc("イベント一覧", reverse("dicon_app:event_list")), bc(event.title)]
    })

def partner_list(request):
    """街の助っ人一覧"""
    partners = Partner.objects.filter(is_active=True)
    return render(request, 'dicon_app/partner_list.html', {
        'partners': partners,
        'crumbs': [bc("街の助っ人")]
    })

def concierge_list(request):
    """コンシェルジュ厳選ピックアップ"""
    items = HomePickup.objects.filter(is_active=True).order_by('order')
    return render(request, 'dicon_app/concierge_list.html', {
        'items': items,
        'crumbs': [bc("厳選ピックアップ")]
    })

def locker_guide(request): 
    """ロッカーの使い方"""
    return render(request, 'dicon_app/locker_guide.html', {'crumbs': [bc("ロッカーガイド")]})

def vacant_store(request): 
    """空き店舗情報"""
    return render(request, 'dicon_app/vacant_store.html', {'crumbs': [bc("空き物件情報")]})

def profile(request): 
    """プロフィール"""
    return render(request, 'dicon_app/profile.html', {'crumbs': [bc("マイページ")]})

def qa(request): 
    """よくある質問"""
    return render(request, 'dicon_app/qa.html', {'crumbs': [bc("よくある質問")]})