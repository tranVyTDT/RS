from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from constrain.choice import SEX
from datetime import datetime, timedelta
import jwt

def get_profile_image_filepatch(self, filename):
    return f'profile_images/{self.pk}/{filename}'

class CustomUser(AbstractUser):
    sex = models.CharField(max_length=6, choices=SEX, blank=True, null=True)
    profile_name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=150, null= True, blank=True)
    phone = models.CharField(max_length=10, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to = get_profile_image_filepatch, null= True, blank=True)

    @property
    def access_token(self):
        token = jwt.encode({ 'id': self.id, 'type': 'access_token', 'username': self.first_name, 'email': self.email, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, algorithm= 'HS256')
        return token
    
    @property
    def refresh_token(self):
        token = jwt.encode({ 'id': self.id, 'type': 'refresh_token', 'username': self.first_name, 'email': self.email, 'exp': datetime.utcnow() + timedelta(days=27)}, settings.SECRET_KEY, algorithm= 'HS256')
        return token
    
    @property
    def account_type(self):
        type = list()
        for group in self.groups.all():
            type.append(group.name)
        return type
