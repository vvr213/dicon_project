from django.db import models
from dicon_app.models import Product

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "決済処理中"),
        ("success", "決済成功"),
        ("cancel", "決済失敗"),
]

    # on_delete=models.PROTECT：商品を消しても注文が壊れないようにする（安全）
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.IntegerField() #金額（今回は product.price を入れる想定）
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending") #決済処理中 success / cancel
    created_at = models.DateTimeField(auto_now_add=True) #作成日時

    def __str__(self):
        return f"Order#{self.id} {self.product.name} {self.status}"