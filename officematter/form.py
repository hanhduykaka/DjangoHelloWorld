from django import forms
from officematter.models import Clients

class FormRegister(forms.ModelForm):
    email=forms.EmailField()
    username=forms.CharField(label='your username',max_length=200) 
    password=forms.CharField(widget = forms.PasswordInput()) 
    confirm=forms.CharField(widget = forms.PasswordInput()) 

    class Meta:
        model=Clients
        fields=['email','username','password']