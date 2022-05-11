from defco.models import DailyLitreRecord, Flag, FuelReplenish, Price, QrCode, Reply, Review, Search, Station, Transaction, User, Vehicle
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(Vehicle)
admin.site.register(Station)
admin.site.register(FuelReplenish)
admin.site.register(Transaction)
admin.site.register(Review)
admin.site.register(Reply)
admin.site.register(QrCode)
admin.site.register(Search)
admin.site.register(Price)
admin.site.register(Flag)
admin.site.register(DailyLitreRecord)

