from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    marks = models.FloatField(null=True, blank=True)
    password_text = models.TextField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.birth_date:
            today = date.today()
            self.age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        super().save(*args, **kwargs)
    
