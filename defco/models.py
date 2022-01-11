from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    rank = models.CharField(max_length = 255)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    svc_no = models.CharField(max_length=255, unique=True)
    mobile = models.CharField(max_length=255, unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    svc_id_img = CloudinaryField('image')
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.username)