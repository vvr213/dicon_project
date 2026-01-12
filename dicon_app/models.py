from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

class Street(models.Model):
    name = models.CharField("通り名", max_length=100, unique=True)
    slug = models.SlugField("スラッグ", max_length=120, unique=True)

    class Meta:
        verbose_name = "通り"
        verbose_name_plural = "通り"

    def __str__(self):
        return self.name


class Shop(models.Model):
    street = models.ForeignKey(
        Street,
        on_delete=models.CASCADE,
        related_name="shops",
        verbose_name="通り",
    )
    name = models.CharField("店舗名", max_length=120)
    description = models.TextField("説明", blank=True)
    line_url = models.URLField("LINEリンク", blank=True, null=True) #1/1LINE追加

    class Meta:
        verbose_name = "店舗"
        verbose_name_plural = "店舗"
        unique_together = ("street", "name")

    def __str__(self):
        return f"{self.street.name} / {self.name}"


class Product(models.Model):
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

    # ✅ 特売（最小）
    is_sale = models.BooleanField("特売", default=False)
    sale_price = models.IntegerField("特売価格", null=True, blank=True)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name


class Set(models.Model):
    """④おすすめセット（献立提案）"""
    name = models.CharField("セット名", max_length=120)
    slug = models.SlugField("スラッグ", max_length=140, unique=True)
    description = models.TextField("説明", blank=True)

    # セットに商品を複数入れる
    products = models.ManyToManyField(Product, related_name="sets", blank=True)

    is_active = models.BooleanField("表示", default=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        verbose_name = "おすすめセット"
        verbose_name_plural = "おすすめセット"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # slug が空なら自動生成（手入力してもOK）
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class HeroSlide(models.Model):
    """トップの告知カルーセル"""
    title = models.CharField("タイトル", max_length=120)
    subtitle = models.CharField("サブタイトル", max_length=200, blank=True)

    # 未入力でも保存できるように blank=True（運用ラク）
    link_url = models.CharField("リンク先URL", max_length=200, blank=True)

    order = models.IntegerField("表示順", default=1)
    is_active = models.BooleanField("表示", default=True)

    class Meta:
        verbose_name = "トップ告知スライド"
        verbose_name_plural = "トップ告知スライド"
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}: {self.title}"

# 1/12追加
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

    start_date = models.DateField("開始日")
    end_date = models.DateField("終了日", blank=True, null=True)

    summary = models.CharField("一言説明", max_length=160, blank=True)
    body = models.TextField("詳細", blank=True)

    category = models.CharField("カテゴリ", max_length=20, choices=CATEGORY_CHOICES, default="season")

    image = models.CharField("画像（staticパス）", max_length=200, blank=True)

    location = models.CharField("場所", max_length=120, blank=True)
    map_url = models.URLField("地図URL", blank=True)

    apply_url = models.URLField("申込URL", blank=True)
    share_text = models.CharField("シェア文（任意）", max_length=120, blank=True)

    is_featured = models.BooleanField("ピックアップ", default=False)
    is_active = models.BooleanField("公開中", default=True)

    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    class Meta:
        ordering = ["start_date", "-created_at"]
        verbose_name = "イベント"
        verbose_name_plural = "イベント"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # slugが空なら自動生成（日本語タイトルでも一旦 slugify で作る）
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("dicon_app:event_detail", kwargs={"slug": self.slug})

    @property
    def is_multi_day(self):
        # 終了日が開始日より後のときだけ「複数日」
        return bool(self.end_date and self.end_date > self.start_date)

    @property
    def is_upcoming(self):
        today = timezone.localdate()
        end = self.end_date or self.start_date
        return end >= today