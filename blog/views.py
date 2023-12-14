
from django.shortcuts import redirect, render
from . import forms
from .models import Ticket
# Create your views here.
def flux_page(request):
    tickets = Ticket.objects.all()
    return render(request, 'flux/flux.html', {'tickets': tickets})

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

    return render(request, 'ticket/ticket.html', {'form': form})