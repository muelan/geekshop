from django.shortcuts import render

import json

# Create your views here.


def index(request):
    context = {'title': 'geekShop'}
    return render(request, 'products/index.html', context)


def products(request):

    title = 'geekShop - каталог'
    f = open('products/fixtures/products.json', encoding='utf-8')
    products = json.load(f)
    context = {'title': title, 'products': products}

    return render(request, "products/products.html", context)