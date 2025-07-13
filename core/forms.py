from django import forms
from .models import TalentRequest, Contact

class TalentRequestForm(forms.ModelForm):
    class Meta:
        model = TalentRequest
        fields = [
            'user_name', 'email', 'phone', 'country',
            'company_name', 'position', 'job_description', 'salary_range'
        ]
        widgets = {
            'job_description': forms.Textarea(attrs={'rows': 4}),
            'salary_range': forms.TextInput(attrs={'placeholder': 'Optional'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['username', 'company_name', 'email', 'phone', 'message']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email address'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone No.'
            }),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your Information Message'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name'}),
        }