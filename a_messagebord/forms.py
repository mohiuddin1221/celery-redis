from django import forms
from django.forms import ModelForm
from .models import *

class MessageModelFrom(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        
