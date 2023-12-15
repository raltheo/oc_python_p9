
from django.shortcuts import redirect, render
from . import forms
from .models import Ticket
from users.utils import get_users_viewable_reviews, get_users_viewable_ticket
from itertools import chain
from django.db.models import CharField, Value

# Create your views here.
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