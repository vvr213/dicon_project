from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError

# ==========================================
# 1. 通り（Street）
# ==========================================
class Street(models.Model):
    name = models.CharField("通り名", max_length=100)
    color = models.CharField("テーマカラー", max_length=20, default="#6c757d", help_text="カラーコード（例：#ff9800）")

    def __str__(self):
        return self.name

# ==========================================
# 2. 店舗（Shop）
# ==========================================
class Shop(models.Model):
    # ▼▼▼ カテゴリ設定（Shopにも追加！） ▼▼▼
    CATEGORY_CHOICES = [
        ('vegetable', '野菜・果物'),
        ('meat', 'お肉・惣菜'),
        ('fish', 'お魚'),
        ('bread', 'パン・ケーキ・菓子'), # 🆕 追加
        ('dry', '乾物・お茶'),          # 🆕 追加
        ('other', 'その他'),
    ]
    category = models.CharField("カテゴリ", max_length=20, choices=CATEGORY_CHOICES, default='other')
    latitude = models.FloatField("緯度", null=True, blank=True, help_text="Googleマップで右クリックしてコピーした緯度（左側の数字）")
    longitude = models.FloatField("経度", null=True, blank=True, help_text="Googleマップで右クリックしてコピーした経度（右側の数字）")
    street = models.ForeignKey(
        Street,
        on_delete=models.CASCADE,
        related_name="shops",
        verbose_name="通り",
    )
    name = models.CharField("店舗名", max_length=120)
    description = models.TextField("説明", blank=True)
    line_url = models.URLField("LINEリンク", blank=True, null=True)
    image = models.ImageField(upload_to='shops/', blank=True, null=True, verbose_name="店舗画像")

    class Meta:
        verbose_name = "店舗"
        verbose_name_plural = "店舗"
        unique_together = ("street", "name")

    def __str__(self):
        return f"{self.street.name} / {self.name}"

# ==========================================
# 3. 商品（Product）
# ==========================================
class Product(models.Model):
    # ▼▼▼ カテゴリ設定（Shopと同じにする） ▼▼▼
    CATEGORY_CHOICES = [
        ('vegetable', '野菜・果物'),
        ('meat', 'お肉・惣菜'),
        ('fish', 'お魚'),
        ('bread', 'パン・ケーキ・菓子'), # 🆕 追加
        ('dry', '乾物・お茶'),          # 🆕 追加
        ('other', 'その他'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    # ▲▲▲ ここまで ▲▲▲

    name = models.CharField("商品名", max_length=100)
    price = models.IntegerField("通常価格")
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="店舗",
        null=True,
        blank=True,
    )

    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="商品画像")
    is_sale = models.BooleanField("特売", default=False)
    sale_price = models.IntegerField("特売価格", null=True, blank=True)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name

# dicon_app/models.py

# ==========================================
# 4. おすすめセット（Set）
# ==========================================
# dicon_app/models.py

class Set(models.Model):
    name = models.CharField("セット名", max_length=120)
    slug = models.SlugField("スラッグ", max_length=140, unique=True)

    # ▼▼▼ この2行が絶対に必要です！ ▼▼▼
    image = models.ImageField(upload_to='sets/', verbose_name='セット画像', blank=True, null=True)
    price = models.IntegerField("セット価格", default=0, help_text="セット全体の税込価格を入力してください")
    # ▲▲▲ ここまで ▲▲▲

    description = models.TextField("説明", blank=True)
    products = models.ManyToManyField(Product, related_name="sets", blank=True)
    is_active = models.BooleanField("表示", default=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        verbose_name = "【管理栄養士】献立セット"
        verbose_name_plural = "【管理栄養士】献立セット"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify 
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# ==========================================
# 5. イベント（Event）
# ==========================================
class Event(models.Model):
    CATEGORY_CHOICES = [
        ("food", "食"),
        ("experience", "体験"),
        ("kids", "子ども"),
        ("sale", "特売"),
        ("season", "季節"),
        ("other", "その他"),
        ("night", "ナイト屋台"),
        ("tasting", "試食リレー"),
        ("retro", "レトロ歓迎"),
        ("rainy", "雨の日"),
    ]

    title = models.CharField("タイトル", max_length=120)
    slug = models.SlugField("スラッグ", max_length=140, unique=True, blank=True)
    start_date = models.DateField("開始日", blank=True, null=True)
    end_date = models.DateField("終了日", blank=True, null=True)
    summary = models.CharField("一言説明", max_length=160, blank=True)
    body = models.TextField("詳細", blank=True)
    category = models.CharField("カテゴリ", max_length=20, choices=CATEGORY_CHOICES, default="season")
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="イベント画像")
    location = models.CharField("場所", max_length=120, blank=True)
    map_url = models.URLField("地図URL", blank=True)
    apply_url = models.URLField("申込URL", blank=True)
    share_text = models.CharField("シェア文（任意）", max_length=120, blank=True)
    is_featured = models.BooleanField("ピックアップ", default=False)
    is_active = models.BooleanField("公開中", default=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    is_regular = models.BooleanField("定番（繰り返し）", default=False, help_text="曜日イベントなど、常時表示したいもの")
    schedule_text = models.CharField("開催パターン（表示用）", max_length=120, blank=True, help_text="例：毎週金曜 17:00〜")
    announce_from = models.DateField("告知開始日", null=True, blank=True, help_text="空なら即表示")
    announce_until = models.DateField("告知終了日", null=True, blank=True, help_text="空ならずっと表示")

    class Meta:
        ordering = ["start_date", "-created_at"]
        verbose_name = "イベント"
        verbose_name_plural = "イベント"

    def clean(self):
        if not self.is_regular and not self.start_date:
            raise ValidationError({"start_date": "スポット（期間/単発）のイベントは開始日が必要です。"})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("dicon_app:event_detail", kwargs={"slug": self.slug})

    @property
    def is_multi_day(self):
        if not self.start_date: return False
        return bool(self.end_date and self.end_date > self.start_date)

    @property
    def is_upcoming(self):
        today = timezone.localdate()
        if self.is_regular: return True
        if not self.start_date: return False
        end = self.end_date or self.start_date
        return end >= today

    @property
    def display_date_text(self):
        if self.is_regular: return self.schedule_text or "定番イベント"
        if not self.start_date: return ""
        if self.end_date and self.end_date > self.start_date:
            return f"{self.start_date} 〜 {self.end_date}"
        return f"{self.start_date}"

# ==========================================
# 6. トップ画像スライド（HeroSlide）
# ==========================================
class HeroSlide(models.Model): # TopSlideからHeroSlideに名前を戻しました（整合性のため）
    title = models.CharField("タイトル", max_length=120)
    subtitle = models.CharField("サブタイトル", max_length=200, blank=True)
    link_url = models.CharField("リンク先URL", max_length=200, blank=True)
    image = models.ImageField(upload_to='slides/', verbose_name="スライド画像", null=True, blank=True)
    order = models.IntegerField("表示順", default=1)
    is_active = models.BooleanField("表示", default=True)

    class Meta:
        verbose_name = "トップ告知スライド"
        verbose_name_plural = "トップ告知スライド"
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}: {self.title}"

# エラー回避用：もしTopSlideという名前で使っていた場合のためのエイリアス
TopSlide = HeroSlide

# 既存のコードの下に追加してください

class HomePickup(models.Model):
    """トップページのピックアップコンテンツ（献立セットや相談など）"""
    title = models.CharField("タイトル", max_length=100)
    description = models.TextField("説明文", max_length=200)
    image = models.ImageField("画像", upload_to='home_pickup/')
    
    # カードの右上に表示するバッジ（例：「4人前」「相談無料」）
    badge_text = models.CharField("バッジテキスト", max_length=50, blank=True)
    
    # 左下の価格表示部分（例：「¥1,800」「プライスレス」）
    price_text = models.CharField("価格テキスト", max_length=50)
    
    # 右下のリンクボタンの文字（例：「レシピ＆購入」「チャットで相談」）
    link_button_text = models.CharField("リンクボタンの文字", max_length=50, default="詳しく見る")
    
    # リンク先のURL（DjangoのURL名を指定、例：'dicon_app:set_list'）
    link_url_name = models.CharField("リンク先のURL名", max_length=100, help_text="例: dicon_app:set_list")

    # 表示順序を指定するための数字
    order = models.IntegerField("表示順序", default=0, help_text="小さい数字ほど前に表示されます")
    # 表示/非表示を切り替えるスイッチ
    is_active = models.BooleanField("公開する", default=True)

    class Meta:
        verbose_name = "【おばちゃん】コンシェルジュ項目"
        verbose_name_plural = "【おばちゃん】コンシェルジュ項目"
        ordering = ['order'] # デフォルトの並び順

    def __str__(self):
        return self.title


# dicon_app/models.py の一番下に追加

# ==========================================
# 7. 【管理栄養士】献立セット (ManagerDietitianSet)
# ==========================================
class ManagerDietitianSet(models.Model):
    # カテゴリの選択肢定義
    CATEGORY_CHOICES = [
        ('beauty', '美容・デトックス'),
        ('health', '健康維持・数値改善'),
        ('speedy', '時短・忙しい人向け'),
        ('diet', '糖質制限・ダイエット'),
        ('reward', '週末のご褒美'),
    ]

    name = models.CharField("セット名", max_length=100)
    slug = models.SlugField("スラッグ", unique=True, help_text="URLの一部になります（例: liver-care）")
    
    # カテゴリフィールド
    category = models.CharField(
        "カテゴリ", 
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='health'
    )

    image = models.ImageField("セット画像", upload_to='sets/', blank=True, null=True)
    price = models.IntegerField("セット価格", default=0, help_text="セット全体の税込価格を入力してください")
    description = models.TextField("説明", blank=True)
    
    # 関連する商品を複数選べるように設定
    products = models.ManyToManyField('Product', verbose_name="セットに含まれる商品", blank=True)
    
    is_active = models.BooleanField("表示", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "【管理栄養士】献立セット"
        verbose_name_plural = "【管理栄養士】献立セット"

    def __str__(self):
        return self.name

# ==========================================
# 8. 認定パートナー（Partner）
# ==========================================
class Partner(models.Model):
    # カテゴリの選択肢定義
    CATEGORY_CHOICES = [
        ('cleaning', 'お掃除'),
        ('repair', '修理・修繕'),
        ('garden', '庭仕事'),
        ('clothing', '洋服・靴'),
        ('painting', '外壁塗装'),  # 追加
        ('helper', 'ヘルパー'),    # 追加
        ('others', 'その他'),      # 追加
    ]

    name = models.CharField("パートナー名", max_length=100)
    
    # ▼ 追加：カテゴリ選択
    category = models.CharField(
        "カテゴリ", 
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='others'
    )

    description = models.TextField("紹介文", blank=True)
    image = models.ImageField("ロゴ・画像", upload_to='partners/', blank=True, null=True)
    url = models.URLField("WebサイトURL", blank=True)
    
    order = models.IntegerField("表示順", default=0)
    is_active = models.BooleanField("表示", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "認定パートナー"
        verbose_name_plural = "認定パートナー"

    def __str__(self):
        return self.name

# ==========================================
# 9. おばちゃんコンシェルジュ項目 (ConciergeItem)
# ==========================================
class ConciergeItem(models.Model):
    title = models.CharField("タイトル（相談内容）", max_length=200)
    answer = models.TextField("おばちゃんの回答")
    order = models.IntegerField("表示順", default=0)
    is_active = models.BooleanField("表示", default=True)

    class Meta:
        verbose_name = "【おばちゃん】コンシェルジュ項目"
        verbose_name_plural = "【おばちゃん】コンシェルジュ項目"

    def __str__(self):
        return self.title

# ==========================================
# 10. 相談メニュー（ホーム画面用）
# ==========================================
class ConsultationItem(models.Model):
    COLOR_CHOICES = [
        ('primary', '青（魚など）'),
        ('danger',  '赤（肉・BBQなど）'),
        ('success', '緑（野菜・下処理など）'),
        ('warning', '黄（カレー・その他）'),
    ]

    title = models.CharField("メニュー名", max_length=100)
    description = models.TextField("説明文")
    image = models.ImageField("画像", upload_to='consult/')
    
    # リンク用（例: fish と入力すると ?preset=fish になります）
    preset_id = models.CharField("プリセットID", max_length=50, help_text="リンク先の識別ID（例: fish, bbq, sasagaki, curry）")
    
    # ボタンの色を選ぶ
    color_theme = models.CharField("テーマカラー", max_length=20, choices=COLOR_CHOICES, default='primary')
    
    order = models.IntegerField("表示順", default=0)
    is_active = models.BooleanField("表示", default=True)

    class Meta:
        verbose_name = "【ホーム】相談メニュー"
        verbose_name_plural = "【ホーム】相談メニュー"
        ordering = ['order']

    def __str__(self):
        return self.title