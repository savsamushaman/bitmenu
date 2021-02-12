from django.forms import ModelForm
from django import forms

from pages.models import ProductCategory, Product


class CategoryForm(ModelForm):
    class_string_c = 'u-black u-border-5 u-border-no-left u-border-no-right u-border-no-top ' \
                     'u-border-palette-1-base u-custom-font u-font-roboto-slab u-input u-input-rectangle'

    class Meta:
        model = ProductCategory
        fields = ['name']

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': class_string_c, 'placeholder': 'Category name : Salads'}), required=True)


class ProductForm(ModelForm):
    class_string_p = 'u-black u-border-5 u-border-no-left u-border-no-right u-border-no-top ' \
                     'u-border-palette-1-base u-custom-font u-font-roboto-slab u-input u-input-rectangle'

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['belongs_to']

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': class_string_p, 'placeholder': 'Name : Pizza Margherita', 'autofocus': 'autofocus'}))

    description = forms.CharField(required=False,
                                  widget=forms.Textarea(
                                      attrs={'class': class_string_p,
                                             'placeholder': 'Description : Mozzarella, Bacon'}))

    price = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2,
                               widget=forms.NumberInput(attrs={'class': class_string_p, 'placeholder': 'Price'}))

    category = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': class_string_p, 'placeholder': 'Category : Pizza'}), required=False,
        queryset=None,
    )

    available = forms.BooleanField(widget=forms.CheckboxInput(), required=False, initial=True)

    def clean(self):
        super(ProductForm, self).clean()

        price = self.cleaned_data.get('price')
        if isinstance(price, type(None)):
            self._errors['price'] = self.error_class(['Price cannot be less than 0'])

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['category'].queryset = ProductCategory.objects.filter(belongs_to=user)
