# from typing_extensions import Required
from datetime import timezone, datetime
import random
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import DateField
from django.forms import DateTimeField
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File
# import datetime

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
    def is_flagged(self):

        if self.flags.filter(flagged=True).exists():
            return True
        
        return False



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
    open = models.BooleanField(default=False)
    admin = models.OneToOneField(User,related_name='station',on_delete=models.CASCADE, default=None)

    def isOpen(self):
        dt = datetime.today()

        # Weekday hours 0900 Hrs to 1800 Hrs
        if dt.weekday() <= 4:
            if dt.hour >= 9 and dt.hour <= 18:
                return True
        # Weekday hours 0900 Hrs to 1700 Hrs
        elif dt.weekday() > 4:
            if dt.hour >= 9 and dt.hour <= 17:
                return True

        return False

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
    description = models.CharField(max_length=1000)
    reveal_id = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']
    
    def __str__(self):
        return 'Review:'+self.review_type+' Transaction:'+str(self.transaction)


class Reply(models.Model):
    description = models.CharField(max_length=1000)
    review = models.ForeignKey(Review,related_name='replies',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='replies',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class QrCode(models.Model):
   url=models.URLField()
   vehicle = models.OneToOneField(Vehicle,related_name='qrcode',on_delete=models.CASCADE, default=False)
   image=models.ImageField(upload_to='qrcode',blank=True)
#    image = transactionsCloudinaryField('image')

   def save(self,*args,**kwargs):
      qrcode_img=qrcode.make(self.url)
      canvas=Image.new("RGB", (375,375),"white")
      draw=ImageDraw.Draw(canvas)
      canvas.paste(qrcode_img)
      buffer=BytesIO()
      canvas.save(buffer,"PNG")
    #   self.image.save(f'image{random.randint(0,9999)}.png',File(buffer),save=False)
      self.image.save(f'QRcode_{self.vehicle}.png',File(buffer),save=False)
      canvas.close()
      super().save(*args,**kwargs)


class Search(models.Model):
    vehicle = models.ForeignKey(Vehicle,related_name='searches',on_delete=models.CASCADE, default=False)
    user=models.ForeignKey(User,related_name='searches',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.vehicle)

class Price(models.Model):
    type = models.CharField(max_length=100)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return self.type + ': Ksh' + str(self.price)

class Flag(models.Model):
    flagged = models.BooleanField(default=False)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User,related_name='flags',on_delete=models.CASCADE)
    reported_by= models.ForeignKey(User,related_name='reported_flags',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-pk']

    def __repr__(self):
        return self.user +':'+ self.description[0:15]
