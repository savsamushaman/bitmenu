from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class MainMenuView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/main_menu.html'
