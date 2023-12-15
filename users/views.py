import re
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from . import forms
from .models import UserFollows
from django.contrib.auth.models import User

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

def abonnement_page(request):
    message = ''
    followers = UserFollows.objects.filter(followed_user=request.user)
    followed_users = UserFollows.objects.filter(user=request.user)
    
    if request.method == 'POST':
        
        form = forms.UserFollowsForm(request.POST)
        if form.is_valid():
            username_to_follow = form.cleaned_data['username']
            user_to_follow = User.objects.get(username=username_to_follow)

            if not UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():
                UserFollows.objects.create(
                    user=request.user,
                    followed_user=user_to_follow
                )
                message = 'Abonnement effectué'
            else:
                message = 'Vous suivez déjà cet utilisateur.'
            return render(request, 'users/abonnement.html', {'form': form, 'message': message, 'followers':followers, 'followed_users':followed_users})
    else:
        form = forms.UserFollowsForm()

    return render(request, 'users/abonnement.html', {'form': form, 'message': message, 'followers':followers, 'followed_users':followed_users})