from django import forms
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'email':   forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'phone':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+263 77 000 0000'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your inquiry about?'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your message here…'}),
        }
