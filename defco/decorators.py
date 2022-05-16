from defco.models import Vehicle
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
            raise PermissionDenied
            # return redirect('home')
       
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
