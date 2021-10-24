from django.db import models
from django.forms.models import ALL_FIELDS
from .models import Give,Profile,ContactUs,states,Vendor
from django.forms import ModelForm, fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import validate_num



class ContactUsForm(ModelForm):
    
    class Meta:
        model= ContactUs
        fields = ('email','subject','ticket','body')


class GiveForm(ModelForm):
    
    class Meta:
        model= Give
        fields = ('name','category','description','image','quantity','state','giver_number','address')
    
class SignupForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password Again'}))
    email = forms.EmailField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    firstname = forms.CharField(max_length= 100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    lastname = forms.CharField(max_length= 100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    username = forms.CharField(max_length= 200,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    phone_number=forms.IntegerField(required=True)
    class Meta:
        model = User
        fields = ('firstname','lastname','username','email','phone_number','password1','password2')

class Profileform(ModelForm):
    
    firstname = forms.CharField(max_length= 100)
    lastname = forms.CharField(max_length= 100)
    email = forms.EmailField(max_length=100)
    phone_number=forms.IntegerField(required=True)
    class Meta:
        model = Profile
        fields = ('profile_pic','firstname','lastname','email','sex','state','phone_number','bio')

class VendorForm(GiveForm):
    state=forms.ChoiceField(widget=forms.Select(attrs={'placeholder':'State of Residence'}),choices=states)
        
    class Meta:
        model = Vendor
        fields=('receiver_number','state','delivery_address')


