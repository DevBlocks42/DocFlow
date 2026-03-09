from django import forms
from apps.documents.models import Document
from .models import Workflow

class CreateWorkflowForm(forms.ModelForm):
    comment = forms.CharField(required=False, label='Commentaire (facultatif)', widget=forms.Textarea(attrs={'class':'form-control', 'rows':3}))
    class Meta:
        model = Workflow
        fields = ["comment"]
        