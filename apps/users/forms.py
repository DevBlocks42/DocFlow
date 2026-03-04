from django import forms
from django.forms.widgets import FileInput
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from apps.utils.validators import validate_secure_image, sanitize_image

User = get_user_model()

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

class UserUpdateForm(forms.ModelForm):
    avatar = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    class Meta: 
        model = User
        fields = ['username', 'email', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            })
        }
        error_messages = {
            'username': {
                'required': "Le nom d'utilisateur est obligatoire.",
                'max_length': "Le nom d'utilisateur est trop long (32 caractères max)."
            },
            'email': {
                'required': "L'email est obligatoire.",
                'invalid': "Veuillez saisir une adresse email valide.",
                'unique': "Cet email est déjà utilisé."
            },
            'avatar': {
                'invalid': 'Veuillez choisir une image valide.'
            }
        }
          
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            avatar = validate_secure_image(avatar)

        else:
            return None
        return avatar        

class EditPasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Mot de passe actuel",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password_confirm = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        currentPassword = cleaned_data.get("current_password")
        newPassword = cleaned_data.get("new_password")
        passwordConfirm = cleaned_data.get("password_confirm")
        if not self.user.check_password(currentPassword):
            raise forms.ValidationError("Le mot de passe actuel est incorrect.")
        if newPassword != passwordConfirm:
            raise forms.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        password_validation.validate_password(newPassword, self.user)
        return cleaned_data

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password"])
        if commit:
            self.user.save()
        return self.user