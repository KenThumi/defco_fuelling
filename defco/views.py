from defco.models import User
from defco.decorators import profile_user, unauthenticated_user
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

@login_required
def customers(request):
    users = User.objects.all().exclude(is_superuser=True)#.latest('date_joined')
    
    return render(request, 'customers.html', {'users':users})

@login_required
@profile_user
def getuser(request, id):
    user = User.objects.get(pk=id)
    return render(request, 'profile.html',{'user':user})