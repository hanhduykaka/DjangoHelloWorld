from django import forms
from officematter.models import Clients,ClientsInformation,Topic,Organization,OrganizationMember,Achievement,Type
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
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


class TopicsForm(forms.ModelForm):    
    top_name = forms.CharField(max_length=100,widget =forms.TextInput(attrs={'class': "input--style-3",'placeholder':"Topic name"}))

    class Meta():
        model = Topic
        fields = ('top_name',)

class OrganizationForm(forms.ModelForm):
    Name = forms.CharField(max_length=200,label="Name",widget = forms.TextInput(attrs={'class': "form-control", 'placeholder':"Name"}))
    Type = forms.ModelChoiceField(queryset=Type.objects.all(),widget = forms.Select(attrs={'class': "form-control"}))
    IsPublic= forms.BooleanField(widget = forms.CheckboxInput(attrs={'class': "form-check-input"}))
    Purpose = forms.CharField(max_length=200,widget = forms.TextInput(attrs={'class': "form-control", 'placeholder':"Purpose"}))
    Image = forms.ImageField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Name'].label = "Organization Name"
        self.fields['Manager'].widget.attrs['class'] = 'form-control'
        self.fields['IsPublic'].required = False
        self.fields['Image'].required = False
        self.fields['Manager'].required = False

    class Meta():
        model = Organization
        fields = ('Name', 'Type', 'IsPublic','Purpose','Manager','Image')