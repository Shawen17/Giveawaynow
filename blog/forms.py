from .models import Comment
from django.forms import ModelForm, fields
from django import forms





class CommentForm(ModelForm):
    
    body = forms.CharField(label='',widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'comment here',
        'rows':2,
        'cols':50,
    }))
    class Meta:
        model = Comment
        fields= ('email','body')

