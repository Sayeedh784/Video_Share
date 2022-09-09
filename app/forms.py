from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import *


class UserSignupForm(UserCreationForm):
  class Meta:
    model = User
    fields= ['email','name','password1', 'password2']



class Video_form(forms.ModelForm):
  class Meta:
    model= PostVideo
    fields=("caption","description","video")