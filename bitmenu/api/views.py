from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from accounts.models import CustomUser
from api.permissions import OwnerWritePerm, OwnsCategoryPerm
from api.serializers import ProductSerializer, CategorySerializer, UserSerializer
from pages.models import Product, ProductCategory


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('api:api_products', request=request, format=format),
        'categories': reverse('api:api_cats', request=request, format=format),
        'users': reverse('api:api_users', request=request, format=format),
    })


class OwnedArticles(generics.ListAPIView):
    serializer_class = None
    queryset = None
    model = None

    def get_queryset(self):
        return self.model.objects.filter(belongs_to=self.request.user)


class ArticleList(generics.ListCreateAPIView):

    def perform_create(self, serializer):
        serializer.save(belongs_to=self.request.user)


# Listings
class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class ProductList(ArticleList):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [OwnsCategoryPerm, ]


class CategoryList(ArticleList):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer


# Details

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [OwnerWritePerm, OwnsCategoryPerm]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [OwnerWritePerm, ]


# owned articles

class OwnedProducts(OwnedArticles):
    model = Product
    serializer_class = ProductSerializer


class OwnedCategories(OwnedArticles):
    model = ProductCategory
    serializer_class = CategorySerializer
