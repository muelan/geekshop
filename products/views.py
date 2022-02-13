from django.shortcuts import render
from .models import Product, ProductCategory

import json

# Create your views here.


def index(request):
    context = {'title': 'geekShop'}
    return render(request, 'products/index.html', context)


def products(request):

    title = 'geekShop - каталог'
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    context = {'title': title, 'products': products, 'categories': categories}

    return render(request, "products/products.html", context)