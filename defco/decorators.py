from defco.models import Station, Transaction, Vehicle
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import HttpResponseRedirect

# Action by admin or superadmin
def superuser(view_func):
    def wrapper_func(request, *args, **kwargs):

        if not request.user.is_superuser :
            # raise PermissionDenied
            messages.error(request, 'Insufficient permission.')
        
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
       
        return view_func(request, *args, **kwargs)
    return wrapper_func

# Redirects login/register routes home if authenticated
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

#bar viewing others profile
def profile_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        id = kwargs['id']

        if request.user.id !=id and not( request.user.is_superuser or  request.user.is_admin):
            messages.error(request, 'Insufficient permission.')
        
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
       
        return view_func(request, *args, **kwargs)
    return wrapper_func


# Action by admin or superadmin
def admin_or_superuser(view_func):
    def wrapper_func(request, *args, **kwargs):

        if not request.user.is_superuser and not request.user.is_admin:
            # raise PermissionDenied
            messages.error(request, 'Insufficient permission.')
        
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
       
        return view_func(request, *args, **kwargs)
    return wrapper_func

# Action by admin or superadmin or attendant
def admin_or_superuser_attendant(view_func):
    def wrapper_func(request, *args, **kwargs):

        if not request.user.is_superuser and not request.user.is_admin and not request.user.is_attendant:
            messages.error(request, 'Insufficient permission.')
        
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
       
        return view_func(request, *args, **kwargs)
    return wrapper_func

# Check account locked 
def account_not_locked(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_locked:
            messages.error(request, 'Your account is locked, contact admin.')           
            return redirect('logout')
        
       
        return view_func(request, *args, **kwargs)
    return wrapper_func

# Check account activated 
def account_activated(view_func):
    def wrapper_func(request, *args, **kwargs):

        if not request.user.is_valid and not request.user.is_superuser:
            messages.error(request, 'Your account is not approved, contact admin.')           
            return redirect('logout')
        
       
        return view_func(request, *args, **kwargs)
    return wrapper_func


#limits user access
def _user(view_func):
    def wrapper_func(request, *args, **kwargs):
      
        # super admit not allowed to insert/edit vehicle
        if not request.user.is_superuser:
            
            if kwargs.get('id') != None:
                id = kwargs.get('id')
                vehicle = Vehicle.objects.get(pk=id)
                
                # Admin cannot edit user vehicle
                if vehicle.user != request.user:
                    messages.error(request, 'Insufficient permission.')
        
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'Insufficient permission.')
        
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
       
        return view_func(request, *args, **kwargs)
    return wrapper_func


#check if admin has a station
def admin_has_station(view_func):
        
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_admin:
            try:
                request.user.station
            except:
                messages.error(request, 'You are not assigned any station yet.')           
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'You are not assigned any station.')           
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
       
        return view_func(request, *args, **kwargs)
    return wrapper_func


# checks the real station admin
def station_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
      
        # super admit not allowed to insert/edit vehicle
        if request.user.is_admin:
            id = kwargs.get('id')

            station = Station.objects.get(pk=id)
            
            try:
                if request.user.station ==station:
                    pass
                else:
                     messages.error(request, ' You are not assigned this station.')
                     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            except:
                messages.error(request, ' You are not assigned any station yet.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
            
        else:
            messages.error(request, 'Permission denied.')           
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        return view_func(request, *args, **kwargs)
    return wrapper_func


#check if admin has a station
def owns_transaction(view_func):
    def wrapper_func(request, *args, **kwargs):

        trans_id = kwargs.get('id')

        trans = Transaction.objects.get(pk=trans_id)

        if request.user != trans.vehicle.user:
            messages.error(request, 'Permission denied. You cant review for other user.')           
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

       
        return view_func(request, *args, **kwargs)
    return wrapper_func


#check if admin has a station
def attendant_transaction(view_func):
    def wrapper_func(request, *args, **kwargs):

        trans_id = kwargs.get('id')

        trans = Transaction.objects.get(pk=trans_id)

        if request.user != trans.attendant:
            messages.error(request, 'Permission denied. You cant edit other attendants transaction.')           
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

       
        return view_func(request, *args, **kwargs)
    return wrapper_func


# station has fuel
# @admin_has_station
def station_has_fuel(view_func):
    def wrapper_func(request, *args, **kwargs):

        replenishment = request.user.station.replenishment.last()
        
        if not bool(replenishment):
            messages.error(request, 'No fuel at your station.')           
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        if replenishment.current_amount == 0:
            messages.error(request, 'No fuel at your station.')           
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

       
        return view_func(request, *args, **kwargs)
    return wrapper_func

