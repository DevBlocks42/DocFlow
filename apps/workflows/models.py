from django.db import models
from apps.documents.models import Document
from apps.users.models import User
from django.utils import timezone

class Workflow(models.Model): 
    STATUS_PENDING = "pending"
    STATUS_VALIDATED = "validated"
    STATUS_ARCHIVED = "archived"
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Soumis'),
        (STATUS_VALIDATED, 'Approuvé'),
        (STATUS_ARCHIVED, 'rejeté')
    ]
    document = models.ForeignKey(Document, on_delete=models.PROTECT, null=False)
    action = models.CharField(choices=STATUS_CHOICES, default=STATUS_PENDING)
    performed_by = models.ForeignKey(User, on_delete=models.PROTECT)
    performed_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField(max_length=255, null=True, blank=True)