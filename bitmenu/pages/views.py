from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.views import View

from pages.forms import CategoryForm
from pages.models import ProductCategory


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


class CreateCategoryView(LoginRequiredMixin, CreateView):
    template_name = 'pages/create_cat.html'
    model = ProductCategory
    form_class = CategoryForm
    success_url = reverse_lazy('pages:create_cat')

    def form_valid(self, form):
        form.instance.belongs_to = self.request.user
        messages.add_message(self.request, messages.INFO, f'{form.instance.name} was created successfully')
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    model = ProductCategory
    context_object_name = 'categories'
    template_name = 'pages/cat_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(belongs_to=self.request.user)
        return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductCategory
    template_name = 'pages/edit_cat.html'
    context_object_name = 'category'
    form_class = CategoryForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        messages.add_message(self.request, messages.INFO, f'Success !')
        return reverse_lazy('pages:update_cat', kwargs={'pk': pk})


class CategoryDelete(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        permission_and_object = check_permission(self, request, ProductCategory)
        if permission_and_object[0]:
            permission_and_object[1].delete()
            return redirect('pages:cat_list')
        return HttpResponseForbidden()
