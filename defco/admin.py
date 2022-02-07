from defco.models import FuelReplenish, Station, User, Vehicle
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(Vehicle)
admin.site.register(Station)
admin.site.register(FuelReplenish)
