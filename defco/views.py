from defco.models import User
from defco.decorators import account_not_locked, admin_or_superuser, profile_user, unauthenticated_user
from defco.forms import UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
@account_not_locked
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
    users = User.objects.filter(is_valid=True, is_locked=False).exclude(is_superuser=True)#.latest('date_joined')
    
    return render(request, 'customers.html', {'users':users})

@login_required
@profile_user
def getuser(request, id):
    user = User.objects.get(pk=id)
    return render(request, 'profile.html',{'user':user})


@login_required
def newapplications(request):
    users = User.objects.filter(is_valid=False).exclude(is_superuser=True)
    
    return render(request, 'newapplications.html', {'users':users})


@login_required
@admin_or_superuser
def approve(request,id):
    User.objects.filter(pk=id).update(is_valid=True)

    return redirect('newapplications')

@login_required
@admin_or_superuser
def lock(request,id):
    User.objects.filter(pk=id).update(is_locked=True)
    return redirect('customers')


@login_required
@admin_or_superuser
def lockusers(request):
    users = User.objects.filter(is_locked=True).exclude(is_superuser=True)
    
    return render(request, 'locked.html', {'users':users})

@login_required
@admin_or_superuser
def unlock(request,id):
    User.objects.filter(pk=id).update(is_locked=False)
    return redirect('lockusers')


def editProfile(request,id):
    user = User.objects.get(pk=id)

    # if request.method=='POST':
    #     form = ImageForm(request.POST,request.FILES)
    
    #     try:
    #         file_to_upload = request.FILES['image']
    #     except:
    #         messages.error(request, 'Kindly select an image.')
           
      
    #     if form.is_valid():
    #         if file_to_upload:
    #             upload_result = cloudinary.uploader.upload(file_to_upload)
    #             new_result = remove_prefix(upload_result['secure_url'],'https://res.cloudinary.com/dtw9t2dom/')

    #         image_result = new_result if new_result else image.image

    #         update_details = {'image':image_result,
    #                            'name':form.cleaned_data['name'],
    #                             'description':form.cleaned_data['description'],
    #                             'category':form.cleaned_data['category'],
    #                             'location':form.cleaned_data['location'] }

    #         Image.update_image(update_details,image_id)

    #         messages.success(request, 'Successful edit.')
    #         return redirect('home')



    form = UserRegisterForm(instance=user)

    ctx = {'form':form}

    return render(request,'registration/updateprofile.html',ctx)