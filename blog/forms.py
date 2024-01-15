from .models import Ticket, Review
from django import forms


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-textarea", "placeholder": "Description"}
            ),
            "image": forms.FileInput(attrs={"class": "form-file"}),
        }


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(str(i), "") for i in range(6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "rating-checkbox"}),
    )

    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
        widgets = {
            "headline": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "body": forms.Textarea(
                attrs={"class": "form-textarea", "placeholder": "Contenu"}
            ),
        }


class FormDeletepost(forms.Form):
    postid = forms.IntegerField(widget=forms.HiddenInput())
    types = forms.CharField(widget=forms.HiddenInput())
