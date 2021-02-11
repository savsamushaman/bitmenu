from django.urls import path
from .views import *

app_name = 'pages'

urlpatterns = [
    path('', AboutView.as_view(), name='about'),
    path('menu/', MainMenuView.as_view(), name='main_menu'),
    path('menu/your_categories/', CategoryListView.as_view(), name='cat_list'),
    path('menu/create_category/', CreateCategoryView.as_view(), name='create_cat'),
    path('menu/update_category/<int:pk>', CategoryUpdateView.as_view(), name='update_cat'),
    path('menu/delete_category/<int:pk>', CategoryDelete.as_view(), name='delete_cat'),

]
