from django.db import models
from apps.documents.models import Document
from apps.users.models import User
from django.utils import timezone

class Workflow(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('pending', 'En validation'),
        ('validated', 'Validé'),
        ('archived', 'Archivé')
    ]
    document = models.ForeignKey(Document, on_delete=models.PROTECT, null=False)
    action = models.CharField(choices=STATUS_CHOICES, default=STATUS_CHOICES[1][1])
    performed_by = models.ForeignKey(User, on_delete=models.PROTECT)
    performed_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField(max_length=255, null=True, blank=True)