from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError

class Street(models.Model):
    # # 通り（例：○○通り）を表すモデル
    name = models.CharField("通り名", max_length=100, unique=True)
    slug = models.SlugField("スラッグ", max_length=120, unique=True)

    class Meta:
        verbose_name = "通り"
        verbose_name_plural = "通り"

    def __str__(self):
        return self.name


class Shop(models.Model):
    # # 店舗モデル：どの通りに属しているか（street）を外部キーで持つ
    street = models.ForeignKey(
        Street,
        on_delete=models.CASCADE,
        related_name="shops",
        verbose_name="通り",
    )
    name = models.CharField("店舗名", max_length=120)
    description = models.TextField("説明", blank=True)
    line_url = models.URLField("LINEリンク", blank=True, null=True)  #1/1LINE追加

    class Meta:
        verbose_name = "店舗"
        verbose_name_plural = "店舗"
        unique_together = ("street", "name")

    def __str__(self):
        return f"{self.street.name} / {self.name}"


class Product(models.Model):
    # # 商品モデル：店舗（shop）にぶら下がる
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
    # # セット（献立提案）モデル：複数の商品を紐づけられる
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
    # # トップページの「固定スライド」用モデル
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
    # # イベントモデル（季節イベント・定番イベントどちらもここに入れる）
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

    # ✅ここが今回の「施工」ポイント
    # # いまは開始日が必須なので、定番イベントを保存すると「このフィールドは必須です」が出る
    # # → 定番イベントは開始日なし運用にしたいので、start_date を任意に変更する
    start_date = models.DateField("開始日", blank=True, null=True)
    # # blank=True：フォーム（admin）で未入力OK
    # # null=True：DB上もNULLを許可（DateFieldはこれがないと保存できない）

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

    # ✅ ここから追加（定番・告知期間）
    is_regular = models.BooleanField(
        "定番（繰り返し）",
        default=False,
        help_text="曜日イベントなど、常時表示したいもの"
    )

    schedule_text = models.CharField(
        "開催パターン（表示用）",
        max_length=120,
        blank=True,
        help_text="例：毎週金曜 17:00〜 / 毎月第2土曜 / 5の付く日"
    )

    announce_from = models.DateField(
        "告知開始日",
        null=True,
        blank=True,
        help_text="空なら即表示"
    )

    announce_until = models.DateField(
        "告知終了日",
        null=True,
        blank=True,
        help_text="空ならずっと表示"
    )
    # ✅ 追加ここまで

    class Meta:
        # ✅ 注意：start_date が NULL になるので ordering に start_date を使うと
        # # DBの並びがちょっと読みづらくなることがある
        # # ただ「いま動いている並び」を崩したくないなら一旦このままでOK
        ordering = ["start_date", "-created_at"]
        verbose_name = "イベント"
        verbose_name_plural = "イベント"

    # 差込場所：Event クラス内（str の上あたり推奨）
    def clean(self):
        # スポット（定番ではない）場合は開始日が必要
        if not self.is_regular and not self.start_date:
            from django.core.exceptions import ValidationError
            raise ValidationError({"start_date": "スポット（期間/単発）のイベントは開始日が必要です。"})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # # slugが空ならタイトルから自動生成
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("dicon_app:event_detail", kwargs={"slug": self.slug})

    @property
    def is_multi_day(self):
        # ✅ start_date が None でも落ちないようにガード
        if not self.start_date:
            return False
        return bool(self.end_date and self.end_date > self.start_date)

    @property
    def is_upcoming(self):
        # ✅ start_date が None の場合は「定番」とみなして True 扱いにしておくと運用が楽
        # # （定番は開催日で期限切れにならないため）
        today = timezone.localdate()
        if self.is_regular:
            return True
        if not self.start_date:
            return False
        end = self.end_date or self.start_date
        return end >= today

    @property
    def display_date_text(self):
        # ✅ テンプレ表示用：定番なら schedule_text を優先、季節なら日付
        # # home.html の「開始日が出ちゃう問題」を、この1つで統一して解決できる
        if self.is_regular:
            return self.schedule_text or "定番イベント"
        # スポット：開始日がないケースは想定外だが、念のため
        if not self.start_date:
            return ""
        # 複数日
        if self.end_date and self.end_date > self.start_date:
            return f"{self.start_date} 〜 {self.end_date}"
        # 単日
        return f"{self.start_date}"

