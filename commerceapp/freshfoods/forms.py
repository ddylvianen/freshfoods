from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *
import unicodedata

class createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2'
                 ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].help_text = ""
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password2'].widget.attrs ={'placeholder': 'Enter your password again, for verification'}

        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = profileUser
        fields = ('img','birthday')
        widgets= {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }


class loginform(forms.Form):
    username = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'login-form-item', 'id': 'Username', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=60, widget=forms.PasswordInput(attrs={'class': 'login-form-item', 'id': 'Password', 'placeholder': 'Password'}))


# class editprofileform(forms.Form):
    # username = forms.CharField()
    # first_name = forms.CharField()
    # last_name = forms.CharField()

    # birthday = forms.CharField()
    # addres = forms.CharField()

    # payment_number = forms.CharField()
    # exp_number = forms.CharField()
    # cvc_number = forms.CharField()
    # cardholder = forms.CharField()
