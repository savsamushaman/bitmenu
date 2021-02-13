from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from accounts.models import CustomUser
from pages.forms import CategoryForm, ProductForm
from pages.models import ProductCategory, Product


def check_permission(self, request, model):
    """checks if the user is allowed to manipulate the object, if yes returns True and the object"""
    user = request.user
    pk = self.kwargs['pk']
    model_object = model.objects.get(pk=pk)
    if model_object.belongs_to == user:
        return True, model_object
    return False, None


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class MainMenuView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/main_menu.html'


class CustomDelView(LoginRequiredMixin, View):
    model = None
    url = None

    def get(self, request, *args, **kwargs):
        permission, model_object = check_permission(self, request, self.model)
        if permission:
            model_object.delete()
            return redirect(self.url)
        return HttpResponseForbidden()


# -- Categories

class CreateCategoryView(LoginRequiredMixin, CreateView):
    template_name = 'pages/create_cat.html'
    model = ProductCategory
    form_class = CategoryForm
    success_url = reverse_lazy('pages:create_cat')

    def form_valid(self, form):
        form.instance.belongs_to = self.request.user
        try:
            form.instance.save()
            messages.add_message(self.request, messages.INFO, f'{form.instance.name} was created successfully')
        except IntegrityError:
            form.add_error('name', 'Category already exists')
            messages.add_message(self.request, messages.INFO, f'{form.instance.name} already exists')
            return super(CreateCategoryView, self).get(self.request, self.args, self.kwargs)
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    model = ProductCategory
    context_object_name = 'categories'
    template_name = 'pages/cat_list.html'

    def get_queryset(self):
        return ProductCategory.objects.filter(belongs_to=self.request.user)


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProductCategory
    template_name = 'pages/edit_cat.html'
    context_object_name = 'category'
    form_class = CategoryForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        messages.add_message(self.request, messages.INFO, f'Success !')
        return reverse_lazy('pages:update_cat', kwargs={'pk': pk})

    def test_func(self):
        return self.get_object().belongs_to == self.request.user


class CategoryDelete(CustomDelView):
    model = ProductCategory
    url = 'pages:cat_list'


# -- Products

class CreateProductView(LoginRequiredMixin, CreateView):
    template_name = 'pages/create_product.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('pages:create_prod')

    def form_valid(self, form):
        form.instance.belongs_to = self.request.user
        try:
            form.instance.save()
            messages.add_message(self.request, messages.INFO, f'{form.instance.name} was created successfully')
        except IntegrityError:
            form.add_error('name', 'Product already exists')
            messages.add_message(self.request, messages.INFO, f'{form.instance.name} already exists')
            return super(CreateProductView, self).get(self.request, self.args, self.kwargs)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateProductView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'pages/product_list.html'

    def get_queryset(self):
        return Product.objects.filter(belongs_to=self.request.user)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'pages/edit_product.html'
    context_object_name = 'product'
    form_class = ProductForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        messages.add_message(self.request, messages.INFO, f'Success !')
        return reverse_lazy('pages:update_prod', kwargs={'pk': pk})

    def test_func(self):
        return self.get_object().belongs_to == self.request.user

    def get_form_kwargs(self):
        kwargs = super(ProductUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ProductDelete(CustomDelView):
    model = Product
    url = 'pages:prod_list'


# -- Menu

class MenuPageView(TemplateView):
    template_name = 'pages/menu_page.html'

    def get_context_data(self, **kwargs):
        context = super(MenuPageView, self).get_context_data(**kwargs)

        user_slug = kwargs.pop('userslug')
        user = get_object_or_404(CustomUser, slug=user_slug)

        context['categories'] = ProductCategory.objects.filter(belongs_to=user)
        context['products'] = Product.objects.filter(belongs_to=user, available=True)
        context['username'] = user.username
        return context
