from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.reverse import reverse

from accounts.models import CustomUser
from api.permissions import OwnerWritePerm, OwnsCategoryPerm
from api.serializers import ProductSerializer, CategorySerializer, UserSerializer, DetailedUserSerializer
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
        try:
            serializer.save(belongs_to=self.request.user)
        except IntegrityError as exc:
            raise APIException(detail=exc)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError as exc:
            raise APIException(detail=exc)


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

class ProductDetail(ArticleDetail):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [OwnerWritePerm, OwnsCategoryPerm]


class CategoryDetail(ArticleDetail):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [OwnerWritePerm, ]


class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = DetailedUserSerializer
    lookup_field = 'username'


# owned articles

class OwnedProducts(OwnedArticles):
    model = Product
    serializer_class = ProductSerializer


class OwnedCategories(OwnedArticles):
    model = ProductCategory
    serializer_class = CategorySerializer


# exceptions
def error_404(request, exception):
    message = 'not found'
    response = JsonResponse(data={'message': message, 'status_code': 404})
    response.status_code = 404
    return response


def error_500(request):
    message = 'internal error'
    response = JsonResponse(data={'message': message, 'status_code': 500})
    response.status_code = 500
    return response
