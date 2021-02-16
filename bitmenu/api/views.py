from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.permissions import OwnerWritePerm
from api.serializers import ProductSerializer
from pages.models import Product, ProductCategory


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('api:api_products', request=request, format=format)
    })


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [OwnerWritePerm, ]

    def perform_update(self, serializer):
        category = self.request.data.get('category', None)
        if category:
            category_owner = ProductCategory.objects.get(pk=category).belongs_to
            if category_owner == self.request.user:
                serializer.save(belongs_to=self.request.user)
                return

        raise PermissionDenied(detail="category belongs to someone else", code=None)


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        category = self.request.data.get('category', None)
        if category:
            category_owner = ProductCategory.objects.get(pk=category).belongs_to
            if category_owner == self.request.user:
                serializer.save(belongs_to=self.request.user)
                return

        raise PermissionDenied(detail="category belongs to someone else", code=None)
