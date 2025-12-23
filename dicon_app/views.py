from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

#一覧表示の中身　商品一覧ページの View
def product_list(request):
    products = Product.objects.all()
    return render(request, "dicon_app/product_list.html", {"products": products})
#③ ブラウザにレスポンスとして返す   ① どのHTMLを使うか決めている       ② どのデータを使うか決めている  ③

#商品詳細ページの View（/products/1/ など）
def product_detail(request, pk): #pk は Product の id のこと（1,2,3…）
    product = get_object_or_404(Product, pk=pk) #存在しないIDなら404にしてくれる
    return render(request, "dicon_app/product_detail.html", {"product": product})