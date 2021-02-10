from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('reg_mail_sent/', RegMailSentView.as_view(), name='r_mail_sent'),
    path('activate/<uidb64>/<token>/', activate_user, name="activate"),
    path('email_confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),

]
