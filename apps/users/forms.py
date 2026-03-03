from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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

class SafeImageField(forms.ImageField):
    default_error_messages = {
        'invalid_image': "Le fichier uploadé n’est pas une image valide."  # ton message en français
    }

    def to_python(self, data):
        try:
            return super().to_python(data)
        except ValidationError:
            # Intercepte l'erreur de Pillow et renvoie notre message
            raise ValidationError(self.error_messages['invalid_image'])

class UserUpdateForm(forms.ModelForm):
    avatar = SafeImageField(
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
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
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
            }
        }
        def clean_avatar(self):
            avatar = self.cleaned_data.get('avatar')
            if avatar:
                # Taille max 2MB
                if avatar.size > 2 * 1024 * 1024:
                    raise ValidationError("Image trop volumineuse (max 2MB).")
                try:
                    img = Image.open(avatar)
                    img.verify()
                except Exception:
                    raise ValidationError("Fichier image invalide.")
                valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
                ext = avatar.name.split('.')[-1].lower()
                if ext not in valid_extensions:
                    raise ValidationError("Format non autorisé.")
            return avatar