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
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', CustomPasswordResetComplete.as_view(), name='password_reset_complete'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),

]
