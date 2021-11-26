from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields

class UserRegisterForm(UserCreationForm): 
        firstName = forms.CharField()     
        lastName = forms.CharField()
        email = forms.EmailField()
        password1 = forms.CharField(label="contraseña", widget=forms.PasswordInput)
        password2 = forms.CharField(label="confirmar contraseña", widget=forms.PasswordInput)
        class Meta:
                model = User
                fields = [
                    "username",
                    "firstName", 
                    "lastName",  
                    "email",
                    "password1",
                    "password2"   
                ]
                                    