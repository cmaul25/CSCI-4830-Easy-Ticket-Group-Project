from django import forms
from django.contrib.auth.models import User

from .models import Ticket, TicketUpdate, UserProfile


class CreateAccountForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'assigned_to']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'assigned_to']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = TicketUpdate
        fields = ['update_text']
        widgets = {
            'update_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a progress update...'}),
        }


class AccountForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']