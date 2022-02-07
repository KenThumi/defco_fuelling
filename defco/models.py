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
    image = CloudinaryField('image',default='https://image.shutterstock.com/image-vector/modern-id-card-photo-man-260nw-1718677939.jpg')
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_joined']

    # class Meta:
    #     permissions = (
    #                 ("make_admin", "Can view and edit most admin features."),
    #                 ("edit_permissions", "Admin user can modify user permissions."),
    #                 ("edit_nacha", "User can edit and modify NACHA files."),
    #                 ("edit_commissions", "User can override commisions."),
    #                 ("view_reports", "User can view admin reports."),
    #                 )
    
    def __str__(self):
        return str(self.username)


class Vehicle(models.Model):
    user = models.ForeignKey(User,related_name='vehicles',on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    image = CloudinaryField('image',default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4m5y8gjoV6xbZvyuHwvOLEYc6tdocBYFdxA&usqp=CAU')
    logbook_no = models.CharField(max_length=255, unique=True, default=None)
    logbook = CloudinaryField('image',default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4m5y8gjoV6xbZvyuHwvOLEYc6tdocBYFdxA&usqp=CAU')
    approval_status = models.BooleanField(default=False)


    def __str__(self):
        return self.reg_no


class Station(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FuelReplenish(models.Model):
    station = models.ForeignKey(Station,related_name='replenishment',on_delete=models.CASCADE)
    current_amount = models.IntegerField()
    replenished_amount = models.IntegerField()
    batch_no = models.CharField(max_length=255)
    supplier = models.CharField(max_length=255)
    
    def __str__(self):
        return self.batch_no

