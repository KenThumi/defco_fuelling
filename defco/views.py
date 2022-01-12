from defco.forms import UserRegisterForm
from django.shortcuts import redirect, render

# Create your views here.

def home(request):
    ctx = {'lorem':'lorem'}
    return render(request,'index.html',ctx)


def register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('home')
    return render(request, 'registration/register.html',{'form':form})
