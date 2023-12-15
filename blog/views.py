
from django.shortcuts import redirect, render
from . import forms
from .models import Ticket
from users.utils import get_users_viewable_reviews, get_users_viewable_ticket

# Create your views here.
def flux_page(request):
    reviews = get_users_viewable_reviews(request.user)
    tickets = get_users_viewable_ticket(request.user)
    print(tickets)
    # tickets = Ticket.objects.all()
    return render(request, 'blog/flux.html', {'tickets': tickets})

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