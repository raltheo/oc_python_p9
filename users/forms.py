from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserFollows
class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d\'utilisateur', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}), label='Mot de passe')


class UserFollowsForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d\'utilisateur', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('User with this username does not exist.')
        return username

class UnfollowForm(forms.Form):
    username = forms.CharField(max_length=63, widget=forms.HiddenInput())