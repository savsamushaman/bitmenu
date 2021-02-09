from django.urls import path
from .views import *

app_name = 'pages'

urlpatterns = [
    path('', AboutView.as_view(), name='about'),
    path('menu/', MainMenuView.as_view(), name='main_menu')
]
