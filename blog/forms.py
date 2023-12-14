from .models import Ticket
from django import forms

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder' : 'Description'}),
            'image': forms.FileInput(attrs={'class': 'form-file'}),
        }