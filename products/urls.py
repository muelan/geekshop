from django.urls import path

from products.views import ProductsListView

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'), # ../products/
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),  # ../products/category/3/
    path('page/<int:page>/', ProductsListView.as_view(), name='page'),  # ../products/page/2/
]