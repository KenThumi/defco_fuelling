from defco.models import User
from defco.decorators import unauthenticated_user
from defco.forms import UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    ctx = {'lorem':'lorem'}
    return render(request,'index.html',ctx)

@unauthenticated_user
def register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('home')
    return render(request, 'registration/register.html',{'form':form})

def customers(request):
    users = User.objects.all().latest('date_joined')
    print(users)
    return render(request, 'customers.html', {'users':users})
