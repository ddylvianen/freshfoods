from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *

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
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = profileUser
        fields = ('img','birthday')
        widgets= {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }


class loginform(forms.Form):
    username = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'login-form-item', 'id': 'Username'}))
    password = forms.CharField(max_length=60, widget=forms.PasswordInput(attrs={'class': 'login-form-item', 'id': 'Password'}))