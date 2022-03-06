from django.shortcuts import render
from .models import Product, ProductCategory

import json

# Create your views here.


def index(request):
    context = {'title': 'geekShop'}
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    context = {'title': 'GeekShop - Каталог',
               'categories': ProductCategory.objects.all(),
               'products': products,
               }

    return render(request, "products/products.html", context)