from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]


class ArtikelForm(forms.ModelForm):
    class Meta:
        model = Artikel
        fields = ["title", "description", "kategori", "date", "img"]

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ["title", "description", "img"]
    