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
    CATEGORY_CHOICES = [
        ('vegetable', '野菜・果物'),
        ('meat', 'お肉・惣菜'),
        ('fish', 'お魚'),
        ('bread', 'パン・ケーキ・菓子'),
        ('dry', '乾物・お茶'),
        ('other', 'その他'),
    ]
    category = models.CharField("カテゴリ", max_length=20, choices=CATEGORY_CHOICES, default='other')
    latitude = models.FloatField("緯度", null=True, blank=True)
    longitude = models.FloatField("経度", null=True, blank=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE, related_name="shops", verbose_name="通り")
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
    CATEGORY_CHOICES = [
        ('vegetable', '野菜・果物'),
        ('meat', 'お肉・惣菜'),
        ('fish', 'お魚'),
        ('bread', 'パン・ケーキ・菓子'),
        ('dry', '乾物・お茶'),
        ('other', 'その他'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    name = models.CharField("商品名", max_length=100)
    price = models.IntegerField("通常価格")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products", verbose_name="店舗", null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="商品画像")
    is_sale = models.BooleanField("特売", default=False)
    sale_price = models.IntegerField("特売価格", null=True, blank=True)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name

# ==========================================
# 4. おすすめセット（Set）
# ==========================================
class Set(models.Model):
    CATEGORY_CHOICES = [
        ('beauty', '美容・デトックス'),
        ('health', '健康維持・数値改善'),
        ('speedy', '時短・忙しい人向け'),
        ('diet', '糖質制限・ダイエット'),
        ('reward', '週末のご褒美'),
    ]
    name = models.CharField("セット名", max_length=120)
    slug = models.SlugField("スラッグ", max_length=140, unique=True, blank=True)
    category = models.CharField("カテゴリ", max_length=20, choices=CATEGORY_CHOICES, default='health')
    image = models.ImageField(upload_to='sets/', verbose_name='セット画像', blank=True, null=True)
    price = models.IntegerField("セット価格", default=0)
    description = models.TextField("説明", blank=True)
    products = models.ManyToManyField(Product, related_name="sets", blank=True)
    is_active = models.BooleanField("表示", default=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    @property
    def total_price(self):
        return self.price

    class Meta:
        verbose_name = "【管理栄養士】献立セット"
        verbose_name_plural = "【管理栄養士】献立セット"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
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
    ]
    title = models.CharField("タイトル", max_length=120)
    slug = models.SlugField("スラッグ", max_length=140, unique=True, blank=True)
    start_date = models.DateField("開始日", blank=True, null=True)
    category = models.CharField("カテゴリ", max_length=20, choices=CATEGORY_CHOICES, default="season")
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="イベント画像")
    is_active = models.BooleanField("公開中", default=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    class Meta:
        verbose_name = "イベント"
        verbose_name_plural = "イベント"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# ==========================================
# 6. トップ画像スライド（HeroSlide）
# ==========================================
class HeroSlide(models.Model):
    title = models.CharField("タイトル", max_length=120)
    image = models.ImageField(upload_to='slides/', verbose_name="スライド画像", null=True, blank=True)
    order = models.IntegerField("表示順", default=1)
    is_active = models.BooleanField("表示", default=True)

    class Meta:
        verbose_name = "トップ告知スライド"
        verbose_name_plural = "トップ告知スライド"
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}: {self.title}"

TopSlide = HeroSlide

# ==========================================
# 7. ピックアップ（HomePickup）
# ==========================================
class HomePickup(models.Model):
    title = models.CharField("タイトル", max_length=100)
    description = models.TextField("説明文", max_length=200)
    image = models.ImageField("画像", upload_to='home_pickup/')
    price_text = models.CharField("価格テキスト", max_length=50, blank=True)
    link_url_name = models.CharField("リンク先のURL名", max_length=100)
    order = models.IntegerField("表示順序", default=0)
    is_active = models.BooleanField("公開する", default=True)

    class Meta:
        verbose_name = "【おばちゃん】コンシェルジュ項目"
        verbose_name_plural = "【おばちゃん】コンシェルジュ項目"
        ordering = ['order']

    def __str__(self):
        return self.title

# ==========================================
# 8. 認定パートナー（Partner）
# ==========================================
class Partner(models.Model):
    CATEGORY_CHOICES = [
        ('cleaning', 'お掃除'),
        ('repair', '修理・修繕'),
        ('others', 'その他'),
    ]
    name = models.CharField("パートナー名", max_length=100)
    category = models.CharField("カテゴリ", max_length=20, choices=CATEGORY_CHOICES, default='others')
    description = models.TextField("紹介文", blank=True)
    image = models.ImageField("ロゴ・画像", upload_to='partners/', blank=True, null=True)
    url = models.URLField("WebサイトURL", blank=True)
    order = models.IntegerField("表示順", default=0)
    is_active = models.BooleanField("表示", default=True)

    class Meta:
        verbose_name = "認定パートナー"
        verbose_name_plural = "認定パートナー"
        ordering = ['order']

    def __str__(self):
        return self.name

# ==========================================
# 9. コンシェルジュ回答（ConciergeItem）
# ==========================================
class ConciergeItem(models.Model):
    title = models.CharField("タイトル", max_length=200)
    answer = models.TextField("おばちゃんの回答")
    order = models.IntegerField("表示順", default=0)
    is_active = models.BooleanField("表示", default=True)

    class Meta:
        verbose_name = "【おばちゃん】コンシェルジュ回答"
        verbose_name_plural = "【おばちゃん】コンシェルジュ回答"
        ordering = ['order']

    def __str__(self):
        return self.title

# ==========================================
# 10. 相談メニュー（ConsultationItem）
# ==========================================
class ConsultationItem(models.Model):
    title = models.CharField("メニュー名", max_length=100)
    description = models.TextField("説明文")
    image = models.ImageField("画像", upload_to='consult/')
    preset_id = models.CharField("プリセットID", max_length=50)
    order = models.IntegerField("表示順", default=0)
    is_active = models.BooleanField("表示", default=True)

    class Meta:
        verbose_name = "【ホーム】相談メニュー"
        verbose_name_plural = "【ホーム】相談メニュー"
        ordering = ['order']

    def __str__(self):
        return self.title