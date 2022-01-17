from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

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
            raise PermissionDenied
            # return redirect('home')
       
        return view_func(request, *args, **kwargs)
    return wrapper_func