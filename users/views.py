from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_POST
from . import forms
from .models import UserFollows, UserBlock
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def logout_page(request):
    logout(request)
    return redirect("login")


def login_page(request):
    if request.user.is_authenticated:
        # User is logged in
        return redirect("flux")
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("flux")
            else:
                message = "Identifiants invalides."
    return render(
        request,
        "users/login.html",
        context={"form": form, "message": message},
    )


def signup_page(request):
    if request.user.is_authenticated:
        # User is logged in
        return redirect("flux")
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect("flux")
    return render(request, "users/register.html", context={"form": form})


@login_required
def abonnement_page(request):
    message = ""
    followers = UserFollows.objects.filter(followed_user=request.user)
    followed_users = UserFollows.objects.filter(user=request.user)
    blocked_user = UserBlock.objects.filter(user=request.user)
    form = forms.UserFollowsForm()
    formblock = forms.BlockForm()
    if request.method == "POST":
        form = forms.UserFollowsForm(request.POST)
        if form.is_valid():
            username_to_follow = form.cleaned_data["username"]
            user_to_follow = User.objects.get(username=username_to_follow)

            if user_to_follow == request.user:
                message = "Vous ne pouvez pas vous suivre vous meme."
                return render(
                    request,
                    "users/abonnement.html",
                    {
                        "form": form,
                        "formblock": formblock,
                        "message": message,
                        "followers": followers,
                        "followed_users": followed_users,
                        "blocked": blocked_user,
                    },
                )

            blocked = UserBlock.objects.filter(
                user=request.user, blocked_user=user_to_follow
            )
            blocked_back = UserBlock.objects.filter(
                user=user_to_follow, blocked_user=request.user
            )
            if blocked.exists() or blocked_back.exists():
                message = "Impossible de suivre un utilisateur bloqué /\
                      qui vous a bloqué"
                return render(
                    request,
                    "users/abonnement.html",
                    {
                        "form": form,
                        "formblock": formblock,
                        "message": message,
                        "followers": followers,
                        "followed_users": followed_users,
                        "blocked": blocked_user,
                    },
                )

            if not UserFollows.objects.filter(
                user=request.user, followed_user=user_to_follow
            ).exists():
                UserFollows.objects.create(
                    user=request.user, followed_user=user_to_follow
                )
                message = "Abonnement effectué"
            else:
                message = "Vous suivez déjà cet utilisateur."
            return render(
                request,
                "users/abonnement.html",
                {
                    "form": form,
                    "formblock": formblock,
                    "message": message,
                    "followers": followers,
                    "followed_users": followed_users,
                    "blocked": blocked_user,
                },
            )

    return render(
        request,
        "users/abonnement.html",
        {
            "form": form,
            "formblock": formblock,
            "message": message,
            "followers": followers,
            "followed_users": followed_users,
            "blocked": blocked_user,
        },
    )


@login_required
@require_POST
def unfollow_page(request):
    try:
        form = forms.UnfollowForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if User.objects.filter(username=username).exists():
                user_to_unfollow = get_object_or_404(User, username=username)
                if user_to_unfollow != request.user:
                    user_follow = UserFollows.objects.filter(
                        user=request.user, followed_user=user_to_unfollow
                    )
                    if user_follow.exists():
                        user_follow.delete()
                        return redirect("abonnement")
    except:
        return redirect("abonnement")


@login_required
@require_POST
def block_page(request):
    try:
        form = forms.BlockForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user_to_block = get_object_or_404(User, username=username)

            if user_to_block == request.user:
                return redirect("abonnement")
            block_relationship = UserBlock.objects.filter(
                user=request.user, blocked_user=user_to_block
            )

            if block_relationship.exists():
                block_relationship.delete()
                return redirect("abonnement")
            else:
                UserBlock.objects.create(
                    user=request.user, blocked_user=user_to_block
                )
                follow = UserFollows.objects.filter(
                    user=request.user, followed_user=user_to_block
                )
                follow_back = UserFollows.objects.filter(
                    user=user_to_block, followed_user=request.user
                )
                if follow.exists():
                    follow.delete()
                if follow_back.exists():
                    follow_back.delete()
                return redirect("abonnement")
        return redirect("abonnement")
    except:
        return redirect("abonnement")
