from unicodedata import name
from defco.decorators import unauthenticated_user
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name='home'),

    # users,authentication
    path('register/', views.register, name='register'),
    path('login/', unauthenticated_user(auth_views.LoginView.as_view(template_name='registration/login.html') ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/login.html'), name='logout'),
    path('customers/', views.customers, name='customers'),
    path('user/<int:id>', views.getuser, name='user'),
    path('newapplications', views.newapplications, name='newapplications'),
    path('approve/<int:id>', views.approve, name='approve'),
    path('lock/<int:id>', views.lock, name='lock'),
    path('lockusers', views.lockusers, name='lockusers'),
    path('unlock/<int:id>', views.unlock, name='unlock'),
    path('editprofile/<int:id>', views.editProfile, name='editprofile'),

    # vehicles
    path('insertvehicle/', views.insertVehicle, name='insertvehicle'),
    path('verifiedvehicles/', views.verifiedVehicles, name='verifiedvehicles'),
    path('unverifiedvehicles/', views.unverifiedVehicles, name='unverifiedvehicles'),
    path('revokevehapproval/<int:id>', views.revokeVehApproval, name='revokevehapproval'),
    path('approveVehicle/<int:id>', views.approveVehicle, name='approvevehicle'),
    path('editvehicle/<int:id>', views.editVehicle, name='editvehicle'),
    path('getvehicle/<int:id>', views.getVehicle, name='getvehicle'),
    path('verifyvehicle', views.verifyVehicle, name="verifyvehicle"),

    # station
    path('addstation/', views.addStation, name='addstation'),
    path('replenishments/', views.replenishments, name='replenishments' ),
    path('stations/', views.stations, name='stations'),
    path('replenish/', views.replenish, name='replenish'),
    path('editstation/<int:id>', views.editStation, name='editstation'),
    path('editreplenish/<int:id>', views.editReplenish, name='editreplenish'),
    path('transactions/', views.getTransactions, name='transactions'),
    path('addtransaction/', views.addTransaction, name='addtransaction'),
    path('edittransaction/<int:id>', views.editTransaction, name='edittransaction'),
    path('switchstationstatus/<int:id>', views.switchStationStatus, name='switchstationstatus'),
    path('adddailyrecords/', views.addDailyRecords, name='adddailyrecords'),
    path('dailyrecords/', views.getDailyRecords, name='dailyrecords'),
    path('deldailyrecord/<int:id>', views.delDailrecord, name='deldailyrecord'),
    
    # reviews
    path('addreview/<int:id>', views.addReview, name='addreview'),
    path('getreviews/', views.getReviews, name='getreviews'),
    path('getspecificreviews/<str:review>', views.getSpecificReviews, name='getspecificreviews'),
    path('setreviewread/<int:id>', views.setReviewRead, name='setreviewread'),
    path('addreply/<int:id>', views.addReply, name='addreply'),

    # qrcode
    path('generateQRCode/<int:id>', views.generateQRCode, name="generateQRCode"),

    #price
    path('addprice/' , views.addPrice, name='addprice'),

    # Flagging
    path('addflag/<int:id>', views.addFlag, name='addflag'),
    path('listflags/', views.listFlags, name='listflags'),
    path('eraseflag/<int:id>', views.eraseFlag, name='eraseflag'),

    # searching / filtering
    path('searchdateranges/<str:target>', views.searchDateRanges, name='searchdateranges' ),
    path('searchdate/', views.searchDate, name='searchdate')
]