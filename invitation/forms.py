# invitations/forms.py
from django import forms
from .models import Invitation


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ["full_name", "company", "email", "phone_number"]

        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Buong Pangalan"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Numero ng Telepono"}
            ),
            "company": forms.Select(attrs={"class": "form-control"}),
        }
