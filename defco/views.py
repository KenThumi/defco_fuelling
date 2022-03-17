from django.http import HttpResponseRedirect
from defco.models import FuelReplenish, Review, Station, Transaction, User, Vehicle
from defco.decorators import _user, account_not_locked, admin_or_superuser, profile_user, unauthenticated_user
from defco.forms import EditVehicleForm, ProfileEditForm, ReplenishForm, ReplyForm, ReviewForm, StationForm, TransactionForm, UserRegisterForm, VehicleForm
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

    if request.method == 'POST':
        form = StationForm(request.POST)

        if form.is_valid():
            form.save()
            # redirect to stations

            messages.success(request, 'Successful Station insertion.')

            return redirect('stations')

    return render(request, 'addstation.html', {'form':form, 'btn_lbl':'Add'})


def editStation(request,id):
    station = Station.objects.get(pk=id)

    form = StationForm(instance=station)

    if request.method == 'POST':
        form = StationForm(request.POST, instance=station)

        if form.is_valid():
            form.save()

            messages.success(request, 'Successful Station update.')
            return redirect('stations')

    return render(request, 'addstation.html', {'form':form,'btn_lbl':'Update'})


def replenishments(request):
    replenishes = FuelReplenish.objects.all()

    return render(request, 'replenishments.html', {'replenishes':replenishes})


def stations(request):
    stations = Station.objects.all()


    return render(request, 'stations.html', { 'stations':stations })


def replenish(request):
    form = ReplenishForm()

    if request.method == 'POST':
        form = ReplenishForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            record.current_amount = form.cleaned_data['replenished_amount']
            record.save()

            messages.success(request, 'Successful resuply recorded.')
            return redirect('replenishments')

    return render(request, 'replenish.html', {'form':form, 'btn_lbl':'Add'})



def editReplenish(request,id):
    replenish = FuelReplenish.objects.get(pk=id)
    form = ReplenishForm(instance=replenish)

    prev_record = replenish.replenished_amount

    if request.method == 'POST':
        form = ReplenishForm(request.POST, instance=replenish)

        if form.is_valid():
            record = form.save(commit=False)

            record.current_amount = replenish.current_amount + (form.cleaned_data['replenished_amount']- prev_record)
            
            record.save()

            messages.success(request, 'Successful edit.')
            return redirect('replenishments')

    return render(request, 'replenish.html', {'form':form, 'btn_lbl':'Update'})



def getTransactions(request):

    transactions = Transaction.objects.all()


    return render(request,'records/transactions.html', {'transactions':transactions})


def addTransaction( request ):

    form = TransactionForm(initial={
                                    'station':request.user.station,
                                    'batch_no':request.user.station.replenishment.latest('id')
                                    }
                            , user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST,  user=request.user)

        if form.is_valid():
            transaction = form.save(commit=False)  
            transaction.attendant = request.user #consider having a 1:n relationship in model
            transaction.save()

            messages.success(request, 'Successful.')
            return redirect('transactions')

    return render(request, 'records/addtransaction.html', {'form':form})



def editTransaction( request, id ):
    transaction = Transaction.objects.get(pk=id)

    form = TransactionForm(user=request.user, instance=transaction)

    if request.method == 'POST':
        form = TransactionForm(request.POST,  user=request.user, instance=transaction)

        if form.is_valid():
            transaction = form.save(commit=False)  
            transaction.attendant = request.user
            transaction.save()

            messages.success(request, 'Successful update.')
            return redirect('transactions')

    return render(request, 'records/addtransaction.html', {'form':form})


def addReview(request, id):
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.transaction = Transaction.objects.get(pk=id)
            review.save()

            messages.success(request, 'Review added successfully.')
            return redirect('getreviews')

    return render(request, 'reviews/review.html', {'form':form})


def getReviews(request):
    reviews = Review.objects.all()#.order_by('-id')

    form = ReplyForm()

    return render(request, 'reviews/reviews.html', {'reviews':reviews, 'form':form})


def getSpecificReviews(request, review):
    reviews = Review.objects.filter(review_type=review)#.order_by('-id')

    form = ReplyForm()

    return render(request, 'reviews/reviews.html', {'reviews':reviews, 'form':form})


def setReviewRead(request,id):
    Review.objects.filter(pk=id).update(is_read=True)

    messages.success(request, 'Review marked as read.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def addReply(request,id):
    if request.method == 'POST':
        form = ReplyForm(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.review_id = id
            reply.user = request.user
            reply.save()

            messages.success(request, 'Reply added successfully.')
            return redirect('getreviews')