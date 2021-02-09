from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    class_string = 'u-border-2 u-border-black u-border-no-left u-border-no-right u-border-no-top u-input ' \
                   'u-input-rectangle u-white'
    username = forms.CharField(widget=forms.TextInput(attrs={'class': class_string, 'placeholder': 'Email',
                                                             }), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': class_string,
                                                                 }), required=True)
