from defco.decorators import unauthenticated_user
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', unauthenticated_user(auth_views.LoginView.as_view(template_name='registration/login.html') ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/login.html'), name='logout'),
    path('customers/', views.customers, name='customers'),
    path('user/<int:id>', views.getuser, name='user'),
    path('newapplications', views.newapplications, name='newapplications'),
    path('approve/<int:id>', views.approve, name='approve'),
    
]