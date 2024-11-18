from django.db import models
import uuid
from django.utils.text import slugify

# Create your models here.
class WeatherUpdate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, null=True)
    location = models.JSONField(null=True)
    current = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f"{self.location.get("name")}"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.country)
        super().save(*args, **kwargs)