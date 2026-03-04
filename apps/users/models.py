from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.utils.validators import validate_secure_image, sanitize_image
import uuid, os


def user_avatar_path(instance, filename):
    ext = "webp"
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("avatars", new_filename)

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, role='employe', **extra_fields):
        if not email:
            raise ValueError("L'email doit être fourni")
        if not username:
            raise ValueError("Le nom d'utilisateur doit être fourni")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, role='admin', **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('employe', 'Employé'),
        ('manager', 'manager'),
        ('admin', 'Administrateur')
    ]
    username = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employe')
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.FileField(upload_to=user_avatar_path, validators=[validate_secure_image], null=True, blank=True)
    service = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        # Si un nouveau fichier est uploadé
        if self.avatar and hasattr(self.avatar, 'file'):
            sanitized_file = sanitize_image(self.avatar.file)
            # Remplace le fichier par la version purifiée
            self.avatar.save(sanitized_file.name, sanitized_file, save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email})"

