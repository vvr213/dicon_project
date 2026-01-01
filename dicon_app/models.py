from django.db import models
from django.utils.text import slugify


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
