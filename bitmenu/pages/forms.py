from django.forms import ModelForm
from django import forms

from pages.models import ProductCategory


class CategoryForm(ModelForm):
    class_string_c = 'u-black u-border-5 u-border-no-left u-border-no-right u-border-no-top ' \
                     'u-border-palette-1-base u-custom-font u-font-roboto-slab u-input u-input-rectangle'

    class Meta:
        model = ProductCategory
        fields = ['name']

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': class_string_c, 'placeholder': 'Category name : Salads'}), required=True)

