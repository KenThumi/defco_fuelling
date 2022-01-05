from django.shortcuts import render

# Create your views here.

def home(request):
    ctx = {'lorem':'lorem'}
    return render(request,'index.html',ctx)