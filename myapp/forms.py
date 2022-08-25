from django import forms
from django.forms import ModelForm
from django.forms import ModelForm,TextInput,FileInput,Select,DateInput
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models  import User
from .models import *

class NewRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,required=True, widget=forms.TextInput(attrs={'placeholder':'username','class':'form-control'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder':'Email','class':'form-control'}))
    password1 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control','data-toggle': 'password','id': 'password',}))
    password2 = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control','data-toggle': 'password','id': 'password',}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder':'username','class':'form-control'}))
    password = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control','data-toggle': 'password','id': 'password',}))

    # class Meta:
    #     model = User
    #     fields = ("username", "password")

class User_More_DetailForm(ModelForm):
    class Meta:
        model = User_More_Detail
        fields = ('first_name','last_name','image','gender','date_of_birth')
        widgets = {
            'first_name': TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name': TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'image': FileInput(attrs={'class':'form-control',"style":"display: none",}),
            'gender':Select(attrs={'class':'form-control',}),
            'date_of_birth':DateInput(attrs={'class':'form-control','placeholder':'Enter a date in this format YYYY-MM-DD'}),
        }