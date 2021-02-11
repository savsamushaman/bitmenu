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
