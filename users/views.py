from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from . import forms

def logout_page(request):
    logout(request)
    return redirect('login')

def login_page(request):
    if request.user.is_authenticated:
        # User is logged in
        return redirect('flux')
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('flux')
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'users/login.html', context={'form': form, 'message': message})

def signup_page(request):
    if request.user.is_authenticated:
        # User is logged in
        return redirect('flux')
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            return redirect('flux')
    return render(request, 'users/register.html', context={'form': form})