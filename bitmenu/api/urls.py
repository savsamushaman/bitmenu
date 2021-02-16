from django.urls import path

from api.views import ProductDetail, ProductList, api_root

app_name = 'api'

urlpatterns = [
    path('', api_root),
    path('products/', ProductList.as_view(), name='api_products'),
    path('products/<int:pk>', ProductDetail.as_view(), name='api_prod_detail')
]
