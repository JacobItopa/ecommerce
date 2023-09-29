from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={
        'placeholder': 'your full name'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'your e-mail'
    }))
    message = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'your message'
    }))