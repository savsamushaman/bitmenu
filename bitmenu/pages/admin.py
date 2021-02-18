from django.contrib import admin

from pages.models import ProductCategory, Product


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'belongs_to', 'pk')
    search_fields = ('name', 'belongs_to__username')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'available', 'belongs_to', 'price', 'category')
    search_fields = ('name', 'belongs_to__username', 'available', 'price', 'category__name')


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
