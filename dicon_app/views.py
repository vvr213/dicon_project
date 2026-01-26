from typing import Optional, Dict
from urllib.parse import urlencode

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

# ▼ 修正点: ManagerDietitianSet と ConsultationItem をインポート
from .models import (
    Shop, Product, Event, HeroSlide, Street, 
    HomePickup, ConciergeItem, Partner, 
    ManagerDietitianSet, ConsultationItem
)

# ==========================================
# 1. 便利な道具（ヘルパー関数）
# ==========================================

def bc(label: str, url: Optional[str] = None) -> Dict[str, Optional[str]]:
    """パンくずリスト作成（必要に応じて使用）"""
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
    
    # 1. ヒーロースライド
    slides = HeroSlide.objects.filter(is_active=True).order_by('order')

    # 2. ピックアップ
    home_pickups = HomePickup.objects.filter(is_active=True).order_by('order')[:6]

    # 3. 本日の特売品
    sale_products = Product.objects.filter(is_sale=True).order_by('?')[:8]

    # ▼ 修正完了: Set -> ManagerDietitianSet
    # 4. 管理栄養士おすすめ献立セット
    recommended_sets = ManagerDietitianSet.objects.filter(is_active=True).order_by('-created_at')[:3]

    # 5. おばちゃんおすすめ献立セット
    concierge_items = ConciergeItem.objects.filter(is_active=True).order_by('order')[:3]

    # 6. おばちゃん下ごしらえ相談（Admin連動）
    consultation_items = ConsultationItem.objects.filter(is_active=True).order_by('order')
    
    # 7. 近日開催のイベント
    today = timezone.localdate()
    upcoming_events = Event.objects.filter(
        is_active=True, 
        start_date__gte=today
    ).order_by('start_date')[:4]
    
    regular_events = []

    # 8. パートナーデータ
    partners = Partner.objects.filter(is_active=True).order_by('order')

    return render(request, 'dicon_app/home.html', {
        'slides': slides,
        'sale_products': sale_products,
        'recommended_sets': recommended_sets,
        'upcoming_events': upcoming_events,
        'regular_events': regular_events,
        'home_pickups': home_pickups,       
        'concierge_items': concierge_items,
        'consultation_items': consultation_items,
        'partners': partners,
    })

# --------------------
# お店一覧
# --------------------
def shop_list(request):
    shops = Shop.objects.all()
    category_slug = request.GET.get('category')

    if category_slug:
        shops = shops.filter(category=category_slug)

    return render(request, 'dicon_app/shop_list.html', {
        'shops': shops,
        'current_category': category_slug, 
    })

# --------------------
# お店詳細
# --------------------
def shop_detail(request, shop_pk):
    shop = get_object_or_404(Shop.objects.select_related("street"), pk=shop_pk)
    products = Product.objects.filter(shop=shop).order_by("name")
    return render(request, "dicon_app/shop_detail.html", {
        "shop": shop,
        "products": products,
    })

# --------------------
# 商品一覧
# --------------------
def product_list(request):
    products = Product.objects.all()
    category_slug = request.GET.get('category')

    if category_slug:
        products = products.filter(category=category_slug)

    return render(request, 'dicon_app/product_list.html', {
        'products': products,
        'current_category': category_slug,
    })

# --------------------
# 商品詳細
# --------------------
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related("shop"), pk=pk)
    return render(request, "dicon_app/product_detail.html", {"product": product})


# ==========================
# 🛒 買い物・カート機能
# ==========================

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('dicon_app:cart_detail')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        
    return redirect('dicon_app:cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total_price = 0
    
    for product_id, quantity in cart.items():
        if str(product_id) == '999':
            class DummyProduct:
                id = 999
                name = '【特別】店長の焼肉おまかせセット(4人前)'
                price = 5000
                is_sale = False
                image = None 
            product = DummyProduct()
            subtotal = product.price * quantity
        else:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                continue

            subtotal = product.price * quantity
            if product.is_sale and product.sale_price:
                 subtotal = product.sale_price * quantity
        
        total_price += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'dicon_app/cart.html', {
        'items': items,
        'total_price': total_price
    })

def checkout(request):
    return render(request, 'dicon_app/checkout.html')

def checkout_done(request):
    if 'cart' in request.session:
        del request.session['cart']
    return render(request, 'dicon_app/checkout_done.html')


# ==========================
# 💬 相談・チャット機能
# ==========================

def consult_menu(request):
    # Adminのデータを使用
    items = ConsultationItem.objects.filter(is_active=True).order_by('order')
    return render(request, 'dicon_app/consult_menu.html', {'items': items})

def consult_home(request):
    # 相談ホーム（プリセット選択時）
    preset_key = request.GET.get('preset')
    
    # 1. まず古いプリセットから探す
    all_presets = _get_consult_presets()
    target_preset = next((p for p in all_presets if p["key"] == preset_key), None)
    
    context = {}
    if target_preset:
        context['preset_title'] = target_preset['title']
        context['preset_desc'] = target_preset['desc']
        
    # 2. DBからも探す（Adminで追加した項目のため）
    elif preset_key:
        try:
            item = ConsultationItem.objects.get(preset_id=preset_key)
            context['preset_title'] = item.title
            context['preset_desc'] = item.description
        except ConsultationItem.DoesNotExist:
            context['preset_title'] = f"{preset_key} についての相談"
            context['preset_desc'] = "この商品について店主に相談します。"
        
    return render(request, 'dicon_app/consult_chat.html', context)

def shop_consult(request, shop_pk):
    shop = get_object_or_404(Shop, pk=shop_pk)
    context = {
        'preset_title': f"{shop.name} への相談",
        'preset_desc': "在庫の確認や取り置きなど、お気軽に話しかけてください。",
    }
    return render(request, 'dicon_app/consult_chat.html', context)

def consult_from_product(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    return redirect(f"{reverse('dicon_app:chat_demo')}?product={product.name}")

def chat_demo(request):
    return render(request, 'dicon_app/chat_demo.html')


# ==========================
# 📅 イベント・特売・その他
# ==========================

def sale_list(request):
    products = Product.objects.filter(is_sale=True).order_by("-id")
    return render(request, "dicon_app/sale_list.html", {"products": products})

def set_list(request):
    # ▼ 修正完了: Set -> ManagerDietitianSet
    sets = ManagerDietitianSet.objects.filter(is_active=True).order_by("-created_at")
    
    category_slug = request.GET.get('category')
    if category_slug:
        sets = sets.filter(category=category_slug)

    context = {
        'sets': sets,
        'current_category': category_slug,
        'categories': ManagerDietitianSet.CATEGORY_CHOICES, # カテゴリ選択肢もモデルから取得
    }
    return render(request, "dicon_app/set_list.html", context)

def set_detail(request, pk=None, slug=None):
    # ▼ 修正完了: Set -> ManagerDietitianSet
    if pk:
        set_obj = get_object_or_404(ManagerDietitianSet, pk=pk, is_active=True)
    elif slug:
        set_obj = get_object_or_404(ManagerDietitianSet, slug=slug, is_active=True)
    else:
        return get_object_or_404(ManagerDietitianSet, pk=None)
        
    return render(request, "dicon_app/set_detail.html", {"set": set_obj})


def event_list(request):
    events = Event.objects.filter(is_active=True).order_by("start_date")
    return render(request, "dicon_app/event_list.html", {"events": events})

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    return render(request, "dicon_app/event_detail.html", {"event": event})

def locker_guide(request):
    return render(request, 'dicon_app/locker_guide.html')

def partner_list(request):
    partners = Partner.objects.filter(is_active=True).order_by('order')
    category_slug = request.GET.get('category')
    
    if category_slug:
        partners = partners.filter(category=category_slug)
        
    context = {
        'partners': partners,
        'current_category': category_slug,
        'categories': Partner.CATEGORY_CHOICES,
    }
    return render(request, 'dicon_app/partner_list.html', context)

def vacant_store(request):
    return render(request, 'dicon_app/vacant_store.html')

def street_list(request):
    streets = Street.objects.all()
    return render(request, "dicon_app/street_list.html", {"streets": streets})

def profile(request):
    return render(request, 'dicon_app/profile.html')

def qa(request):
    return render(request, 'dicon_app/qa.html')

def concierge_list(request):
    items = HomePickup.objects.filter(is_active=True).order_by('order')
    return render(request, 'dicon_app/concierge_list.html', {'items': items})