from defco.forms import UserRegisterForm
from django.shortcuts import render

# Create your views here.

def home(request):
    ctx = {'lorem':'lorem'}
    return render(request,'index.html',ctx)


def register(request):
    form = UserRegisterForm()

    # if request.method == 'POST':

    return render(request, 'registration/register.html',{'form':form})
