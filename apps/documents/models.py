from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.utils.validators import validate_document_file
import uuid, os

def user_document_path(instance, filename):
    ext = os.path.splitext(filename)[1] 
    new_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("documents", new_filename)

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PENDING = "pending"
    STATUS_VALIDATED = "validated"
    STATUS_ARCHIVED = "archived"
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Brouillon'),
        (STATUS_PENDING, 'En validation'),
        (STATUS_VALIDATED, 'Validé'),
        (STATUS_ARCHIVED, 'Archivé')
    ]
    title = models.CharField(max_length=64)
    description = models.TextField()
    file = models.FileField(upload_to=user_document_path, validators=[validate_document_file])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents_created')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents_assigned')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title