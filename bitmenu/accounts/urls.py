from django.urls import path
from .views import FirstView

app_name = 'accounts'

urlpatterns = [
    path('', FirstView.as_view(), name='first')
]
