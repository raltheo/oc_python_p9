
from django.shortcuts import get_object_or_404, redirect, render
from . import forms
from django.views.decorators.http import require_POST
from .models import Ticket, Review
from users.utils import get_users_viewable_reviews, get_users_viewable_ticket
from itertools import chain
from django.db.models import CharField, Value
from django.contrib.auth.decorators import login_required
import os


# Create your views here.
@login_required
def flux_page(request):
    reviews, no_review = get_users_viewable_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    #https://stackoverflow.com/questions/1107737/numeric-for-loop-in-django-templates/63624984#63624984 => pour la loop dans la template
    #pour template fontawesome user homive4111@aseall.com password : password
    no_review = no_review.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_users_viewable_ticket(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    unique_tickets = []
    for ticket in tickets: #check si le ticket a deja une revue si oui on le prend pas en tant que ticket mais en tant que revue 
        if not ticket.review_set.exists(): #https://docs.djangoproject.com/en/5.0/topics/db/queries/ search for _set
            unique_tickets.append(ticket)
    posts = sorted(
        chain(reviews, unique_tickets, no_review), ## merci le cahier des charges xD (a moitié au final mdr)
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'blog/flux.html', {'posts': posts})

@login_required
def ticket_page(request):
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    else:
        form = forms.TicketForm()

    return render(request, 'blog/ticket.html', {'form': form})

@login_required
def post_page(request):
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, "blog/post.html", {'posts': posts})

@login_required
def review_page(request):
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)

        if review_form.is_valid() and ticket_form.is_valid():
            
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('flux')

    else:
        review_form = forms.ReviewForm()
        ticket_form = forms.TicketForm()

    return render(request, 'blog/review.html', {'review_form': review_form, 'ticket_form': ticket_form})

@login_required
@require_POST
def deletepost(request):
    #https://docs.djangoproject.com/en/3.1/topics/http/shortcuts/#get-object-or-404
    
    form = forms.FormDeletepost(request.POST)
    if form.is_valid():
        types = form.cleaned_data['types']
        postid = form.cleaned_data['postid']
        if types == "review":
            review = get_object_or_404(Review, id=postid)
            if review.user == request.user:
                review.delete()
        if types == "ticket":
            ticket = get_object_or_404(Ticket, id=postid)
            if ticket.user == request.user:
                if ticket.image:
                    os.remove(ticket.image.path)
                ticket.delete()
    return redirect("post")

@login_required
def reply_page(request):###pas ouf avec le get or 404 error if str, mais bon 
    try:
        if request.method == "POST":
            ticket = get_object_or_404(Ticket, id=request.POST.get("ticketid"))
            review_form = forms.ReviewForm(request.POST)
            if review_form.is_valid():            
                review = review_form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                review.save()
                return redirect('flux')
        elif request.GET.get("ticketid"):
            ticket = get_object_or_404(Ticket, id=request.GET.get("ticketid"))
            review_form = forms.ReviewForm()
            return render(request, 'blog/replyticket.html', {'review_form': review_form, 'ticket': ticket})
    except:
        return redirect('flux')

@login_required
def modify_page(request):

    try:
        post = request.GET.get("type")
        post_id = request.GET.get("id")
        if post == "TICKET":
            ticket = get_object_or_404(Ticket, id=post_id)
            if request.user == ticket.user:
                if request.method == "POST":
                    ticket_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
                    if ticket_form.is_valid():
                        ticket_form.save()
                        return redirect("flux")
                    
                ticket_form = forms.TicketForm(instance=ticket) #https://stackoverflow.com/questions/2236691/how-do-i-display-the-value-of-a-django-form-field-in-a-template
                return render(request, "blog/modify.html", {"ticket" : ticket, "ticket_form": ticket_form})
            
        if post == "REVIEW":
            review = get_object_or_404(Review, id=post_id)
            if request.user == review.user:
                if request.method == "POST":
                    review_form = forms.ReviewForm(request.POST, instance=review)
                    if review_form.is_valid():
                        review_form.save()
                        return redirect("flux")

                review_form = forms.ReviewForm(instance=review)
                return render(request, "blog/modify.html", {"review" : review, "review_form" : review_form})
            
        return redirect("flux")
    except:
        return redirect("flux")