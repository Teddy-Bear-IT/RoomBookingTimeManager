from django.contrib.auth.forms import AuthenticationForm
from django import forms

from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm):
    username= forms.CharField(widget=forms.TextInput(attrs={
        "type"    : 'text',
        "placeholder":'Введите логин',
        'class' : 'form-block__input-item',
        'required':True,

    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type"    : 'password',
        "placeholder":'Введите пароль',
        'class' : 'form-block__input-item',
        'required':True,

    }))

    class Meta:
        model = User
        fields = ('username','password')

