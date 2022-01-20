from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import HttpResponseRedirect

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

        if request.user.id !=id and not request.user.is_superuser:
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
