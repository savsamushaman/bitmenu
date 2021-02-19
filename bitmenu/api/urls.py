from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import *

app_name = 'api'

urlpatterns = [
    path('', api_root),
    path('products/', ProductList.as_view(), name='api_products'),
    path('products/<int:pk>', ProductDetail.as_view(), name='api_prod_detail'),
    path('products/owned/', OwnedProducts.as_view(), name='api_prod_owned'),
    path('cats/', CategoryList.as_view(), name='api_cats'),
    path('cats/<int:pk>', CategoryDetail.as_view(), name='api_cats_detail'),
    path('cats/owned', OwnedCategories.as_view(), name='api_cats_owned'),
    path('users/', UserList.as_view(), name='api_users'),
    path('users/<str:username>', UserDetail.as_view(), name='api_user_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
