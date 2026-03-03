from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        error_messages={
            "required": "L'adresse email est requise.",
            "invalid": "Veuillez entrer une adresse email valide."
        },
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "john.doe@docflow.com" 
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        error_messages={
            "required": "Le mot de passe est requis."
        },
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )
    error_messages = {
        'invalid_login': "Email ou mot de passe incorrect. Veuillez réessayer.",
        'inactive': "Ce compte est désactivé."
    }