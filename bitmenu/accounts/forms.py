from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms

from accounts.models import CustomUser


# class string is repeated, in case a form needs visual change

class LoginForm(AuthenticationForm):
    class_string = 'u-border-2 u-border-black u-border-no-left u-border-no-right ' \
                   'u-border-no-top u-input u-input-rectangle u-white '

    username = forms.CharField(widget=forms.TextInput(attrs={'class': class_string, 'placeholder': 'Username',
                                                             }), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': class_string,
                                                                 }), required=True)


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    class_string_reg = 'u-border-2 u-border-black u-border-no-left u-border-no-right' \
                       ' u-border-no-top u-input u-input-rectangle u-white'

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': class_string_reg}),
                               required=True)

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': class_string_reg}),
                             required=True)

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': class_string_reg,
                                                                  }), required=True)

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password again', 'class': class_string_reg,
                                          }), required=True)

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        username = cleaned_data.get('username')
        if username and CustomUser.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        return cleaned_data


class CustomPassRecMailForm(PasswordResetForm):
    class_string_res_mail = 'u-border-2 u-border-black u-border-no-left u-border-no-right ' \
                            'u-border-no-top u-input u-input-rectangle u-white'

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': class_string_res_mail}),
                             required=True)


class CustomSetPassForm(SetPasswordForm):
    class_string_res_pass = 'u-border-2 u-border-black u-border-no-left u-border-no-right u-border-no-top u-input ' \
                            'u-input-rectangle u-white'

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': class_string_res_pass,
                                          }), required=True)

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': class_string_res_pass,
                                          }), required=True)
