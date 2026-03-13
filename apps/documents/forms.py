from django import forms
from .models import Document, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateDocumentForm(forms.ModelForm):
    title = forms.CharField(
        label="Titre du document",
        error_messages={
            'required': 'Veuillez saisir un titre.',
            'max_length': 'Le titre dépasse la limite de caractères'
        },
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        label="Description",
        error_messages={
            'required': 'Veuillez saisir une description.',
            'max_length': 'La description dépasse la limite de caractères.'
        },
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':3})
    )
    file = forms.FileField(
        label="Fichier",
        required=True,
        error_messages={
            'required': 'Veuillez sélectionner un fichier.',
            'invalid': 'Le fichier téléchargé est invalide.'
        },
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(role='manager'),
        label="Assigner à",
        widget=forms.Select(attrs={'class':'form-select'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Catégorie",
        widget=forms.Select(attrs={'class':'form-select'})
    )

    class Meta:
        model = Document
        fields = ['title', 'description', 'file', 'category', 'assigned_to']

    def clean_assigned_to(self):
        user = self.cleaned_data.get('assigned_to')
        if user and user.role != 'manager':
            raise ValidationError("Seul un utilisateur avec le rôle 'manager' peut être assigné à ce document.")
        return user