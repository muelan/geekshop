from django.urls import path

from products.views import products

app_name = 'products'

urlpatterns = [
    path('', products, name='index'), # ../products/
    path('category/<int:category_id>/', products, name='category'),  # ../products/category/3/
    path('page/<int:page>/', products, name='page'),  # ../products/page/2/
]