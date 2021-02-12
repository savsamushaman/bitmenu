from decimal import Decimal

from django.db import models
from django.utils.text import slugify

from accounts.models import CustomUser


class ProductCategory(models.Model):
    belongs_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    class Meta:
        unique_together = ('belongs_to', 'name')


class Product(models.Model):
    belongs_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    available = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=Decimal('0')), name='price_gt_0'),
        ]
        unique_together = ('belongs_to', 'name')

    def __str__(self):
        return str(self.name)
