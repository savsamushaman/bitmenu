from rest_framework import serializers

from accounts.models import CustomUser
from pages.models import Product


class ProductSerializer(serializers.ModelSerializer):
    belongs_to = serializers.ReadOnlyField(source='belongs_to.username')

    class Meta:
        model = Product
        fields = ['name', 'available', 'description', 'price', 'category', 'belongs_to']

# class UserSerializer(serializers.ModelSerializer):
#     products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
#
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'products']
