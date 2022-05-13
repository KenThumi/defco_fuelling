from main.settings import BASE_URL
from django.http import HttpResponseRedirect
from defco.models import DailyLitreRecord, Flag, FuelReplenish, Price, QrCode, Review, Search, Station, Transaction, User, UserApproval, UserLock, Vehicle, VehicleApproval
from defco.decorators import _user, account_activated, account_not_locked, admin_or_superuser, profile_user, unauthenticated_user
from defco.forms import DailyRecordForm, EditVehicleForm, FlagForm, PriceForm, ProfileEditForm, ReplenishForm, ReplyForm, ReviewForm, StationForm, TransactionForm, UserRegisterForm, VehicleForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from datetime import  datetime, date, timedelta

# Create your views here.
@login_required
@account_not_locked
@account_activated
def home(request):
    # get recent search results
    searches = Search.objects.filter(user=request.user)

    # get  stations
    stations = 0

    station = Station.objects.all().last() 

    if station.isOpen():  # find out if its official operating hours
        stations = Station.objects.filter(open=True).count( )

    # petroleum price
    petroleum = Price.objects.filter(type='petroleum').last()

    # petroleum price
    diesel = Price.objects.filter(type='diesel').last()

    # active flags
    flags = Flag.objects.filter(flagged=True).count()

    # users
    users = User.objects.filter(is_customer=True).count()

    # new applications
    applications = User.objects.filter(is_valid=False).exclude(is_superuser=True).count()

    # locked users
    locked = User.objects.filter(is_locked=True).exclude(is_superuser=True).count()

    #  Approved Vehicles
    vehicles = Vehicle.objects.filter(approval_status=True).count()

    # unverifiedvehicles
    unverifiedvehicles = Vehicle.objects.filter(approval_status=False).count()

    # lowfuel (<=1000)
    qr_set = FuelReplenish.objects.order_by('station','-created_at').distinct('station')
    
    lowfuel = 0  #count of station with fuel below 1000 l

    for x in qr_set:
        if x.current_amount <= 1000:
            lowfuel+=1

    # Reviews
    complaints = Review.objects.filter(review_type='complaint').count()

    recommendations = Review.objects.filter(review_type='recommendation').count()

    comments = Review.objects.filter(review_type='comment').count()

    unread = Review.objects.filter(is_read=False).count()


    # ctx
    ctx = {
            'searches':searches, 'stations':stations, 'petroleum':petroleum, 
            'diesel':diesel, 'flags':flags, 'users':users, 
            'applications':applications, 'locked':locked,
            'vehicles':vehicles, 'unverifiedvehicles':unverifiedvehicles,
            'lowfuel':lowfuel, 'complaints':complaints,
            'recommendations':recommendations,'comments':comments,
            'unread':unread
          }

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
    
    return render(request, 'customers.html', {'users':users, 'target':'customers'})

@login_required
@profile_user
def getuser(request, id):
    user = User.objects.get(pk=id)

    # user vehicles
    vehicles = Vehicle.objects.filter(user=user)

    return render(request, 'profile.html',{'user':user, 'vehicles':vehicles})


@login_required
@admin_or_superuser
def newapplications(request):
    users = User.objects.filter(is_valid=False).exclude(is_superuser=True)
    
    return render(request, 'newapplications.html', {'users':users, 'target':'newapplications'})


@login_required
@admin_or_superuser
def approve(request,id):
    User.objects.filter(pk=id).update(is_valid=True)


    # record dates
    UserApproval.objects.create(user=User.objects.get(pk=id))

    messages.success(request, 'User approved successfully.')
    return redirect('newapplications')

@login_required
@admin_or_superuser
def lock(request,id):
    User.objects.filter(pk=id).update(is_locked=True)

    # record lock 
    UserLock.objects.create(user=User.objects.get(pk=id))

    messages.success(request, 'User account has been locked successfully.')
    return redirect('customers')


@login_required
@admin_or_superuser
def lockusers(request):
    users = User.objects.filter(is_locked=True).exclude(is_superuser=True)
    
    return render(request, 'locked.html', {'users':users, 'target':'locked'})

@login_required
@admin_or_superuser
def unlock(request,id):
    User.objects.filter(pk=id).update(is_locked=False)

     # remove lock record from Userlock model
    UserLock.objects.filter(user=User.objects.get(pk=id)).delete()

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
            vehicle.reg_no = request.POST.get('reg_no').replace(' ','').lower()
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

    # record vehicleapproval
    ## if records exist
    record = VehicleApproval.objects.filter(vehicle=Vehicle.objects.get(pk=id))
    if record:
        
        VehicleApproval.objects.filter(vehicle=Vehicle.objects.get(pk=id)).update(created_at=datetime.now())
    else:
        VehicleApproval.objects.create(vehicle=Vehicle.objects.get(pk=id))

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

            # Deduct from main readings
            current_readings= FuelReplenish.objects.filter(batch_no = form.cleaned_data['batch_no']).last()
            current_readings.current_amount =  current_readings.current_amount - int( form.cleaned_data['litres'] )

            current_readings.save()

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


# QRCode

def getVehicle(request,id):
    try:
        vehicle = Vehicle.objects.get(pk=id)
    except Vehicle.DoesNotExist:
        raise Http404('No Vehicle matches the given query')
    
    return render(request, 'vehicles/vehicle.html',{'vehicle':vehicle})

# generateQRCode
def generateQRCode(request,id):
    qrcode_url= BASE_URL+'/getvehicle/'+str(id)

    QrCode.objects.create(url=qrcode_url, vehicle=Vehicle.objects.get(pk=id))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#verify
def verifyVehicle(request):
    if request.method == 'POST':
        reg_no = request.POST.get('vehicle','') 

        if reg_no:
            #reg_no = ''.join(vehicle.split())  # remove all white spaces

            reg_no = reg_no.replace(' ','').lower() # remove all white spaces

            # * validation further needed
            try:
                veh = Vehicle.objects.filter(reg_no=reg_no).first()
            except Vehicle.DoesNotExist:
                raise Http404('No Vehicle matches the given query')

            if veh == None:
                messages.error(request, 'No Vehicle matches the given query.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            recordSearch(request,veh.id)

            return redirect(f'/getvehicle/{veh.id}') # get the vehicle

        else:
            messages.error(request, 'Empty search. Please fill the search field.')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# record recent searchs
def recordSearch(request,id):
    vehicle = Vehicle.objects.get(pk=id)

    Search.objects.create(vehicle = vehicle, user=request.user)



# close / open station
def switchStationStatus(request, id):

    dt = datetime.today()

    # Weekday hours 0900 Hrs to 1800 Hrs
    if dt.weekday() <= 4:
        if dt.hour >= 9 and dt.hour <= 18:
            pass
        else:

            messages.error(request, 'Unofficial Hours.')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # Weekday hours 0900 Hrs to 1700 Hrs
    elif dt.weekday() > 4:
        if dt.hour >= 9 and dt.hour <= 17:
            pass
        else:

            messages.error(request, 'Unofficial Hours.')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    
    station = Station.objects.get(pk = id)

    station.open = not station.open

    station.save()

    messages.success(request, 'Successfully recorded.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# adding prices
def addPrice(request):
    form = PriceForm()

    if request.method == 'POST':
        form = PriceForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Price added successfully.')
            return redirect('home')

    return render(request, 'price/price.html', {'form':form})


# flagging customers ***GET request prone manipulation, consider hidden input
def addFlag(request,id):
    form = FlagForm()

    if request.method == 'POST':
        form = FlagForm(request.POST)

        if form.is_valid():
            flag = form.save(commit=False)
            flag.flagged = True
            flag.user = get_object_or_404(User, id=id)
            flag.reported_by = request.user
            flag.save()

            messages.success(request, 'Flag added successfully.')
            return redirect('/user/'+str(id))

    return render(request, 'flags/flagForm.html', {'form':form})



# list flags
def listFlags(request):
    flags = Flag.objects.all()

    return render(request, 'flags/allFlags.html', {'flags':flags})


# erase flag
def eraseFlag(request, id):
    Flag.objects.filter(pk=id).update(flagged=False)

    messages.success(request, 'Flag erased successfully.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#add daily records
def addDailyRecords(request):

    form = DailyRecordForm(
                            initial={
                                    'station':request.user.station,
                                    }
                            )

    if request.method == 'POST':
        form = DailyRecordForm(request.POST)
        # print(request.POST)
        # return
        if form.is_valid():
            form.save()  

            messages.success(request, 'Successful Insertion')
            return redirect('dailyrecords')

    return render(request, 'records/dailyreadingsform.html', {'form':form})


# getDailyRecords
def getDailyRecords(request):
    records = DailyLitreRecord.objects.all()

    return render(request, 'records/dailyreadings.html', {'records':records} )


# delete Records
def delDailrecord(request, id):
    record = DailyLitreRecord.objects.get(pk=id)

    record.delete()

    messages.success(request, 'Successful Deletion')

    return redirect('dailyrecords')



# search/filter
def searchDateRanges(request, target ):
    
    if request.POST:
        #get the dates
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        # str to datetime instance 
        from_date = datetime.strptime(from_date, '%m/%d/%Y')
        to_date = datetime.strptime(to_date, '%m/%d/%Y') + timedelta(hours=23, minutes=59,seconds = 59, milliseconds=999)

        # validate
        if to_date < from_date:
            messages.error(request,'From date cannot be earlier than To date')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        # to a manipulatable str >> for model querying
        from_date = from_date.strftime('%Y-%m-%d')
        to_date = to_date.strftime('%Y-%m-%d')

        # if search is on customers
        if target == 'customers':
            users = User.objects.filter(date_joined__range = [from_date,to_date],is_valid=True, is_locked=False).exclude(is_superuser=True)#.latest('date_joined')
        
            return render(request, 'customers.html', {'users':users, 'target':'customers'})
        # if search is on newapplications
        elif target == 'newapplications':
            users = User.objects.filter(date_joined__range = [from_date,to_date],is_valid=False).exclude(is_superuser=True)
    
            return render(request, 'newapplications.html', {'users':users, 'target':'newapplications'})
        # if search is locked - mean filter by time when users were locked
        elif target == 'locked':
            users = User.objects.filter(userlock__created_at__range = [from_date,to_date],is_locked=True).exclude(is_superuser=True)
    
            return render(request, 'locked.html', {'users':users, 'target':'locked'})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))