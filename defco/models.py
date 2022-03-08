# from typing_extensions import Required
from datetime import timezone
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import DateField
from django.forms import DateTimeField

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
    is_attendant = models.BooleanField(default=False)

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
    admin = models.OneToOneField(User,related_name='station',on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name


class FuelReplenish(models.Model):
    station = models.ForeignKey(Station,related_name='replenishment',on_delete=models.CASCADE)
    current_amount = models.IntegerField(default=0)
    replenished_amount = models.IntegerField()
    batch_no = models.CharField(max_length=255)
    supplier = models.CharField(max_length=255)

    class Meta:
        ordering = ['-pk']
    
    def __str__(self):
        return self.batch_no


class Transaction(models.Model):
    vehicle = models.ForeignKey(Vehicle,related_name='transactions',on_delete=models.CASCADE)
    litres = models.IntegerField()
    amount = models.IntegerField()
    payment_mode = models.CharField(max_length=255)
    station = models.ForeignKey(Station,related_name='transactions',on_delete=models.CASCADE)
    batch_no = models.ForeignKey(FuelReplenish,related_name='transactions',on_delete=models.CASCADE)
    attendant = models.ForeignKey(User,related_name='transactions',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']
    
    def __str__(self):
        return 'Veh:'+self.vehicle.reg_no+' Litres:'+str(self.litres)+' Batch no:'+self.batch_no.batch_no


class Review(models.Model):
    user=models.ForeignKey(User,related_name='reviews',on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction,related_name='reviews',on_delete=models.CASCADE)
    review_type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']
    
    def __str__(self):
        return 'Review:'+self.review_type+' Transaction:'+str(self.transaction)
