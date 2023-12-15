
import re
from django.shortcuts import get_object_or_404, redirect, render
from . import forms
from .models import Ticket, Review
from users.utils import get_users_viewable_reviews, get_users_viewable_ticket
from itertools import chain
from django.db.models import CharField, Value
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def flux_page(request):
    reviews = get_users_viewable_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_users_viewable_ticket(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    unique_tickets = []
    for ticket in tickets: #check si le ticket a deja une revue si oui on le prend pas en tant que ticket mais en tant que revue 
        if not ticket.review_set.exists(): #https://docs.djangoproject.com/en/5.0/topics/db/queries/ search for _set
            unique_tickets.append(ticket)
    posts = sorted(
        chain(reviews, unique_tickets), ## merci le cahier des charges xD (a moitié au final mdr)
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

def post_page(request):
    return render(request, "blog/post.html")

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
                 
                ticket.delete()
    return redirect("flux")


def reply_page(request):
    try:
        if request.POST:
            ticket = get_object_or_404(Ticket, id=request.POST.get("ticketid"))
            review_form = forms.ReviewForm(request.POST)
            if review_form.is_valid():            
                review = review_form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                review.save()

                return redirect('flux')
        if request.GET.get("ticketid"):
            ticket = get_object_or_404(Ticket, id=request.GET.get("ticketid"))
            review_form = forms.ReviewForm()
            return render(request, 'blog/replyticket.html', {'review_form': review_form, 'ticket': ticket})
    except:
        return redirect('flux')
    
        

    return redirect("flux")