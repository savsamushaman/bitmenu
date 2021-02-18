from rest_framework import serializers

from accounts.models import CustomUser
from pages.models import Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='belongs_to.username')

    class Meta:
        model = Product
        fields = ['owner', 'id', 'name', 'category', 'price', 'available', 'description', ]


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='belongs_to.username')

    class Meta:
        model = ProductCategory
        fields = ['owner', 'name', 'id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'id']
