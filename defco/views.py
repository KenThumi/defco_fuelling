from defco.models import User, Vehicle
from defco.decorators import _user, account_not_locked, admin_or_superuser, profile_user, unauthenticated_user
from defco.forms import EditVehicleForm, ProfileEditForm, StationForm, UserRegisterForm, VehicleForm
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
@admin_or_superuser
def customers(request):
    users = User.objects.filter(is_valid=True, is_locked=False).exclude(is_superuser=True)#.latest('date_joined')
    
    return render(request, 'customers.html', {'users':users})

@login_required
@profile_user
def getuser(request, id):
    user = User.objects.get(pk=id)
    return render(request, 'profile.html',{'user':user})


@login_required
@admin_or_superuser
def newapplications(request):
    users = User.objects.filter(is_valid=False).exclude(is_superuser=True)
    
    return render(request, 'newapplications.html', {'users':users})


@login_required
@admin_or_superuser
def approve(request,id):
    User.objects.filter(pk=id).update(is_valid=True)

    messages.success(request, 'User approved successfully.')
    return redirect('newapplications')

@login_required
@admin_or_superuser
def lock(request,id):
    User.objects.filter(pk=id).update(is_locked=True)

    messages.success(request, 'User account has been locked successfully.')
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

    messages.success(request, 'User account has been unlocked successfully.')
    return redirect('lockusers')

@login_required
@profile_user
def editProfile(request,id):
    user = User.objects.get(pk=id)

    form = ProfileEditForm(instance=user)

    ctx = {'form':form}

    if request.method=='POST':
        form = ProfileEditForm(request.POST,request.FILES, instance=user)
    
        # try:
        #     file_to_upload = request.FILES['image']
        # except:
        #     messages.error(request, 'Kindly select an image.')
           
      
        if form.is_valid():
            form.save()

            messages.success(request, 'Successful edit.')
            return redirect('customers')

        else:
            messages.warning(request, 'Some errors occurred. Check them below.')

            ctx = {'form':form}

    return render(request,'registration/updateprofile.html',ctx)

@_user
def insertVehicle(request):
    form = VehicleForm()

    ctx = {'form':form, 'btn_label':'Add'}

    if request.method == 'POST':
        v_form = VehicleForm(request.POST, request.FILES)

        if v_form.is_valid():
            vehicle = v_form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()

            messages.success(request, 'Successful insertion.')
            return redirect('unverifiedvehicles')
        else:
            ctx = {'form':v_form}

    return render(request, 'insertVehicle.html',ctx)


def unverifiedVehicles(request):
    vehicles = Vehicle.objects.filter(approval_status=False)

    return render(request, 'vehicles/unverifiedVehicles.html', {'vehicles':vehicles})


def verifiedVehicles(request):
    vehicles = Vehicle.objects.filter(approval_status=True)

    return render(request, 'vehicles/verifiedVehicles.html', {'vehicles':vehicles})



def revokeVehApproval(request, id):
    Vehicle.objects.filter(pk=id).update(approval_status=False)

    messages.success(request, 'Approval successfully revoked.')

    return redirect('verifiedvehicles')



def approveVehicle(request, id):
    Vehicle.objects.filter(pk=id).update(approval_status=True)

    messages.success(request, 'Successful Vehicle Approval.')

    return redirect('unverifiedvehicles')


@_user
def editVehicle(request,id):
    vehicle = Vehicle.objects.get(pk=id)

    v_form = EditVehicleForm(instance=vehicle)

    if request.method == 'POST':
        v_form = EditVehicleForm(request.POST, request.FILES, instance = vehicle)

        if v_form.is_valid():
            v_form.save()

            return redirect('verifiedvehicles')

    return render(request, 'insertVehicle.html', {'form':v_form, 'btn_label':'Update'})



def addStation(request):
    form = StationForm()

    return render(request, 'addstation.html', {'form':form})