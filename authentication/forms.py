from django import forms
from django.forms import TextInput
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d\'utilisateur', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}), label='Mot de passe')