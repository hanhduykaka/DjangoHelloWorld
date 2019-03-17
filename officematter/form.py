from django import forms
from officematter.models import Clients,ClientsInformation
from django.contrib.auth.models import User

class FormRegister(forms.ModelForm):
    email=forms.EmailField()
    username=forms.CharField(label='your username',max_length=200) 
    password=forms.CharField(widget = forms.PasswordInput()) 
    confirm=forms.CharField(widget = forms.PasswordInput()) 

    class Meta:
        model=Clients
        fields=['email','username','password']

class UserForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'class': "input--style-3", 'placeholder':"Username"}))
    email=forms.CharField(widget = forms.EmailInput(attrs={'class': "input--style-3",'placeholder':"Email"}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': "input--style-3",'placeholder':"Password"}))
    confirm=forms.CharField(widget = forms.PasswordInput(attrs={'class': "input--style-3",'placeholder':"Confirm-password"}))

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
    

class UserProfileInfoForm(forms.ModelForm):    
    bio = forms.CharField(label='your username',max_length=500,widget = forms.TextInput(attrs={'class': "input--style-3",'placeholder':"Bio-information"}))

    class Meta():
        model = ClientsInformation
        fields = ('bio',)