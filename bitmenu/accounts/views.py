from django.shortcuts import render
from django.views.generic import TemplateView


class FirstView(TemplateView):
    template_name = 'accounts/base.html'
