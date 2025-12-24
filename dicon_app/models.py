from django.db import models

# Create your models here.

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

    class Meta:
        verbose_name = "店舗"
        verbose_name_plural = "店舗"
        unique_together = ("street", "name")

    def __str__(self):
        return f"{self.street.name} / {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="店舗",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name