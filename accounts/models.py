from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
import uuid


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    
    Role = {
        ('admin', 'admin'),
        ('user', 'user')
    }
    
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name   = models.CharField(max_length=255)
    last_name    = models.CharField(max_length=255)
    image        = models.ImageField(upload_to='images/', null=True)
    email        = models.EmailField(unique=True)
    password     = models.CharField(max_length=255)
    role         = models.CharField(max_length=255, choices=Role)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted   = models.BooleanField(default=False)
    date_joined  = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.email} -- {self.id}"
