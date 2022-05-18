from main.settings import BASE_URL
from django.http import HttpResponseRedirect
from defco.models import Attendant, DailyLitreRecord, Flag, FuelReplenish, Price, QrCode, Review, Search, Station, Transaction, User, UserApproval, UserLock, Vehicle, VehicleApproval
from defco.decorators import _user, account_activated, account_not_locked, admin_has_station, admin_or_superuser, admin_or_superuser_attendant, attendant_transaction, owns_transaction, profile_user, station_admin, station_has_fuel, superuser, unauthenticated_user
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

    if bool(station):  #stations exists
        if station.isOpen():  # find out if its official operating hours
            stations = Station.objects.filter(open=True).count( )

    # petroleum price
    petroleum = Price.objects.filter(type='petroleum').last()

    # petroleum price
    diesel = Price.objects.filter(type='diesel').last()

    # active flags
    flags = Flag.objects.filter(flagged=True).count()

    ## admin
    if request.user.is_admin:
        flags = Flag.objects.filter(user__unit=request.user.unit,flagged=True).count()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        flags = Flag.objects.filter(user=request.user,flagged=True).count()

    # ----------------- USERS --------------------------------------------------------Q
    # users
    # users = User.objects.filter(is_customer=True).exclude(is_superuser=True).count()
    users = User.objects.filter(is_customer=True, is_valid=True, is_locked=False).exclude(is_superuser=True).count()

    ## admin
    if request.user.is_admin:
        users = User.objects.filter(unit=request.user.unit,is_customer=True, is_valid=True, is_locked=False).exclude(is_superuser=True).count()

    # new applications
    applications = User.objects.filter(is_valid=False).exclude(is_superuser=True).count()

    ## admin
    if request.user.is_admin:
        applications = User.objects.filter(unit=request.user.unit,is_valid=False).exclude(is_superuser=True).count()

    # locked users
    locked = User.objects.filter(is_locked=True).exclude(is_superuser=True).count()
    ## admin
    if request.user.is_admin:
        locked = User.objects.filter(unit=request.user.unit,is_locked=True).exclude(is_superuser=True).count()
    
    # ----------------VEHICLES---------------------------------------
    #  Approved Vehicles
    vehicles = Vehicle.objects.filter(approval_status=True).count()
    ## admin
    if request.user.is_admin:
        vehicles = Vehicle.objects.filter(user__unit = request.user.unit,approval_status=True).count()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        vehicles = Vehicle.objects.filter(user = request.user,approval_status=True).count()

    # unverifiedvehicles
    unverifiedvehicles = Vehicle.objects.filter(approval_status=False).count()
    ## admin
    if request.user.is_admin:
        unverifiedvehicles = Vehicle.objects.filter(user__unit = request.user.unit,approval_status=False).count()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        unverifiedvehicles = Vehicle.objects.filter(user = request.user,approval_status=False).count()

    # ----------------- FUEL ------------------------------------------------------------
    # lowfuel (<=1000)
    qr_set = FuelReplenish.objects.order_by('station','-created_at').distinct('station')
    
    lowfuel = 0  #count of station with fuel below 1000 l

    for x in qr_set:
        if x.current_amount <= 1000:
            lowfuel+=1

    # ----------------- REVIEWS ----------------------------------------------------------
    # Reviews

    complaints = Review.objects.filter(review_type='complaint').count()

    ## admin unread from particular station
    if request.user.is_admin:
        complaints= Review.objects.filter(transaction__station__admin=request.user ,review_type='complaint').count()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        complaints= Review.objects.filter(user=request.user ,review_type='complaint').count()


    recommendations = Review.objects.filter(review_type='recommendation').count()

    ## admin unread from particular station
    if request.user.is_admin:
        recommendations= Review.objects.filter(transaction__station__admin=request.user ,review_type='recommendation').count()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        recommendations= Review.objects.filter(user=request.user ,review_type='recommendation').count()


    comments = Review.objects.filter(review_type='comment').count()

    ## admin unread from particular station
    if request.user.is_admin:
        comments= Review.objects.filter(transaction__station__admin=request.user ,review_type='comment').count()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        comments= Review.objects.filter(user=request.user ,review_type='comment').count()


    unread = Review.objects.filter(is_read=False).count()

    ## admin unread from particular station
    if request.user.is_admin:
        unread= Review.objects.filter(transaction__station__admin=request.user ,is_read=False).count()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        unread= Review.objects.filter(user=request.user ,is_read=False).count()

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
            
            messages.success(request, 'Registration successful, pending verification and approval.')

            return redirect('login')
    return render(request, 'registration/register.html',{'form':form})

@login_required
@admin_or_superuser
def customers(request):
    users = User.objects.filter(is_valid=True, is_locked=False).exclude(is_superuser=True)#.latest('date_joined')
    
    ## admin
    if request.user.is_admin:
        users = User.objects.filter(unit=request.user.unit,is_customer=True, is_valid=True, is_locked=False).exclude(is_superuser=True, id=request.user.id)


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

    ## admin
    if request.user.is_admin:
        users = User.objects.filter(unit=request.user.unit,is_valid=False).exclude(is_superuser=True)

    
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

    ## admin
    if request.user.is_admin:
        users = User.objects.filter(unit=request.user.unit,is_locked=True).exclude(is_superuser=True)

    
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

        
            return redirect('login')

        else:
            messages.warning(request, 'Some errors occurred. Check them below.')

            ctx = {'form':form}

    return render(request,'registration/updateprofile.html',ctx)

@_user
@login_required
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

@login_required
def unverifiedVehicles(request):
    vehicles = Vehicle.objects.filter(approval_status=False)

    ## admin
    if request.user.is_admin:
        vehicles = Vehicle.objects.filter(user__unit = request.user.unit,approval_status=False)
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        vehicles = Vehicle.objects.filter(user= request.user,approval_status=False)

    return render(request, 'vehicles/unverifiedVehicles.html', {'vehicles':vehicles})

@login_required
def verifiedVehicles(request):
    vehicles = Vehicle.objects.filter(approval_status=True)

    # admin
    if request.user.is_admin:
        vehicles = Vehicle.objects.filter(user__unit = request.user.unit,approval_status=True)
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        vehicles = Vehicle.objects.filter(user= request.user,approval_status=True)
    

    return render(request, 'vehicles/verifiedVehicles.html', {'vehicles':vehicles, 'target':'veh_verified'})

@login_required
@admin_or_superuser
def revokeVehApproval(request, id):
    Vehicle.objects.filter(pk=id).update(approval_status=False)

    #update revoke time
    VehicleApproval.objects.filter(vehicle=Vehicle.objects.get(pk=id)).update(created_at=datetime.now())

    messages.success(request, 'Approval successfully revoked.')

    return redirect('verifiedvehicles')


@login_required
@admin_or_superuser
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


@superuser
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

@superuser
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

@admin_or_superuser_attendant
def replenishments(request):
    replenishes = FuelReplenish.objects.all()

    ## admin
    if request.user.is_admin:
        try:
            replenishes = FuelReplenish.objects.filter(station=request.user.station).all()
        except:
            replenishes = ''

    return render(request, 'replenishments.html', {'replenishes':replenishes, 'target':'replenishes'})

@login_required
def stations(request):
    stations = Station.objects.all()


    return render(request, 'stations.html', { 'stations':stations })

@login_required
@admin_has_station
def replenish(request):
    form = ReplenishForm(
                            initial = {
                                    'station':request.user.station
                            }
                        )

    if request.method == 'POST':
        form = ReplenishForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)

            # forbit zero entry
            if form.cleaned_data['replenished_amount'] == 0:
                messages.error(request, 'Replenishment cannot be Zero.')           
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            record.current_amount = form.cleaned_data['replenished_amount']
            record.save()

            messages.success(request, 'Successful resuply recorded.')
            return redirect('replenishments')

    return render(request, 'replenish.html', {'form':form, 'btn_lbl':'Add'})

@admin_or_superuser
@admin_has_station
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


@login_required
def getTransactions(request):

    transactions = Transaction.objects.all()

    # admin 
    if request.user.is_admin:
        transactions = Transaction.objects.filter(station__admin =request.user ).all()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        transactions = Transaction.objects.filter(vehicle__user =request.user ).all()

    return render(request,'records/transactions.html', {'transactions':transactions,'target':'transactions'})

@login_required
@admin_or_superuser_attendant
@admin_has_station
@station_has_fuel
def addTransaction( request ):

    form = TransactionForm(initial={
                                    'station':request.user.station,
                                    'batch_no':request.user.station.replenishment.latest('id')
                                    }
                            , user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST,  user=request.user)

        veh = Vehicle.objects.get(pk=request.POST.get('vehicle'))

        # check if vehicle is verified
        if not veh.approval_status:
                messages.error(request, 'Vehicle not verified.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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

@login_required
@admin_or_superuser_attendant
@attendant_transaction
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

@login_required
@owns_transaction
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

@login_required
def getReviews(request):
    reviews = Review.objects.all()#.order_by('-id')

    # admin
    if request.user.is_admin:
        reviews = Review.objects.filter(transaction__station=request.user.station).all()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        reviews = Review.objects.filter(user=request.user).all()


    form = ReplyForm()

    return render(request, 'reviews/reviews.html', {'reviews':reviews, 'form':form, 'target':'reviews'})

@login_required
def getSpecificReviews(request, review):
    reviews = Review.objects.filter(review_type=review)#.order_by('-id')

    # admin
    if request.user.is_admin:
        reviews = Review.objects.filter(review_type=review, transaction__station=request.user.station).all()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        reviews = Review.objects.filter(user=request.user,review_type=review,).all()


    form = ReplyForm()

    return render(request, 'reviews/reviews.html', {'reviews':reviews, 'form':form, 'target':'None'})

@login_required
@admin_or_superuser
def setReviewRead(request,id):
    # check if the right admin in charge of station on focus
    review = Review.objects.get(pk=id)

    if str(review.transaction.station) != str(request.user.station):
        messages.error(request, 'Your account is not approved, contact admin.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    Review.objects.filter(pk=id).update(is_read=True)

    messages.success(request, 'Review marked as read.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@admin_or_superuser
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
@login_required
@admin_or_superuser_attendant
def getVehicle(request,id):
    try:
        vehicle = Vehicle.objects.get(pk=id)
    except Vehicle.DoesNotExist:
        raise Http404('No Vehicle matches the given query')
    
    return render(request, 'vehicles/vehicle.html',{'vehicle':vehicle})

# generateQRCode
@login_required
def generateQRCode(request,id):
    qrcode_url= BASE_URL+'/getvehicle/'+str(id)

    QrCode.objects.create(url=qrcode_url, vehicle=Vehicle.objects.get(pk=id))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#verify
@login_required
@admin_or_superuser_attendant
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
@login_required
@admin_or_superuser_attendant
def recordSearch(request,id):
    vehicle = Vehicle.objects.get(pk=id)

    Search.objects.create(vehicle = vehicle, user=request.user)



# close / open station
@station_admin
@login_required
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
@superuser
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
@admin_or_superuser_attendant
@login_required
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
@login_required
def listFlags(request):
    flags = Flag.objects.all()

    if request.user.is_admin:
        flags = Flag.objects.filter(reported_by__unit=request.user.unit).all()
    elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
        flags = Flag.objects.filter(user=request.user).all()

    return render(request, 'flags/allFlags.html', {'flags':flags, 'target':'flags'})


# erase flag
@admin_or_superuser_attendant
@login_required
def eraseFlag(request, id):
    Flag.objects.filter(pk=id).update(flagged=False)

    messages.success(request, 'Flag erased successfully.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


#add daily records
@admin_has_station #****************************************************************
def addDailyRecords(request):

    form = DailyRecordForm(
                            initial={
                                    'station':request.user.station,
                                    }
                            )

    if request.method == 'POST':
        form = DailyRecordForm(request.POST)
        
        # check if its actual station admin
        station_id = request.POST.get('station')
    
        if int(request.user.station.id) != int(station_id):
            messages.error(request, 'You are not assigned this station.')           
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


        if form.is_valid():
            form.save()  

            messages.success(request, 'Successful Insertion')
            return redirect('dailyrecords')

    return render(request, 'records/dailyreadingsform.html', {'form':form})


# getDailyRecords
@admin_has_station
@login_required
def getDailyRecords(request):
    records = DailyLitreRecord.objects.all()

    # admin
    if request.user.is_admin:
        records = DailyLitreRecord.objects.filter(station=request.user.station).all()

    return render(request, 'records/dailyreadings.html', {'records':records, 'target':'dailyrecords'} )


# delete Records
@login_required
@admin_or_superuser_attendant
def delDailrecord(request, id):
    record = DailyLitreRecord.objects.get(pk=id)

    record.delete()

    messages.success(request, 'Successful Deletion')

    return redirect('dailyrecords')



# search/filter
@login_required
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
        

        # if search is on customers
        if target == 'customers':
            users = User.objects.filter(date_joined__gte = from_date, date_joined__lte = to_date,is_valid=True, is_locked=False).exclude(is_superuser=True)#.latest('date_joined')
            
            # admin
            if request.user.is_admin:
                users = User.objects.filter(unit=request.user.unit,date_joined__gte = from_date, date_joined__lte = to_date,is_valid=True, is_locked=False).exclude(is_superuser=True)#.latest('date_joined')

            return render(request, 'customers.html', {'users':users, 'target':'customers'})
        # if search is on newapplications
        elif target == 'newapplications':
            users = User.objects.filter(date_joined__gte = from_date, date_joined__lte = to_date,is_valid=False).exclude(is_superuser=True)

             # admin
            if request.user.is_admin:
                users = User.objects.filter(unit=request.user.unit,date_joined__gte = from_date, date_joined__lte = to_date,is_valid=False).exclude(is_superuser=True)

            return render(request, 'newapplications.html', {'users':users, 'target':'newapplications'})
        # if search is 'locked' - mean filter by time when users were locked
        elif target == 'locked':
            users = User.objects.filter(userlock__created_at__gte = from_date,userlock__created_at__lte =to_date,is_locked=True).exclude(is_superuser=True)
    
            # admin
            if request.user.is_admin:
                users = User.objects.filter(unit=request.user.unit,userlock__created_at__gte = from_date,userlock__created_at__lte =to_date,is_locked=True).exclude(is_superuser=True)

            return render(request, 'locked.html', {'users':users, 'target':'locked'})
        # if search is 'veh_verified' - mean filter by time when veh were verfified/approved
        elif target =='veh_verified':
            vehicles = Vehicle.objects.filter(vehicleapproval__created_at__gte = from_date,vehicleapproval__created_at__lte = to_date,approval_status=True)
            # admin
            if request.user.is_admin:
                vehicles = Vehicle.objects.filter(user__unit=request.user.unit,vehicleapproval__created_at__gte = from_date,vehicleapproval__created_at__lte = to_date,approval_status=True)
            elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
                vehicles = Vehicle.objects.filter(user=request.user,vehicleapproval__created_at__gte = from_date,vehicleapproval__created_at__lte = to_date,approval_status=True)

            return render(request, 'vehicles/verifiedVehicles.html', {'vehicles':vehicles, 'target':'veh_verified'})
        # if search is 'replenishes
        elif target == 'replenishes':
            replenishes = FuelReplenish.objects.filter(created_at__gte = from_date, created_at__lte = to_date).all()

             # admin
            if request.user.is_admin:
                try:
                    replenishes = FuelReplenish.objects.filter(station=request.user.station, created_at__gte = from_date, created_at__lte = to_date).all()
                except:
                    replenishes = ''

            return render(request, 'replenishments.html', {'replenishes':replenishes, 'target':'replenishes'})
        
        # if search is transactions
        elif target == 'transactions':
            transactions = Transaction.objects.filter(date__gte = from_date, date__lte = to_date).all()
             # admin
            if request.user.is_admin: # 
                transactions = Transaction.objects.filter(station__admin =request.user,date__gte = from_date, date__lte = to_date).all()
            elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
                transactions = Transaction.objects.filter(vehicle__user =request.user,date__gte = from_date, date__lte = to_date).all()

            return render(request,'records/transactions.html', {'transactions':transactions,'target':'transactions'})
        # if search is dailyrecords
        elif target == 'dailyrecords':
            records = DailyLitreRecord.objects.filter(created_at__gte = from_date, created_at__lte = to_date).all()
             # admin
            if request.user.is_admin:
                records = DailyLitreRecord.objects.filter(station=request.user.station,created_at__gte = from_date, created_at__lte = to_date).all()
            
            return render(request, 'records/dailyreadings.html', {'records':records, 'target':'records'} )
        # search reviews,
        elif target == 'reviews':
            reviews = Review.objects.filter(created_at__gte = from_date, created_at__lte = to_date).all()
             # admin
            if request.user.is_admin:
                reviews = Review.objects.filter(transaction__station=request.user.station,created_at__gte = from_date, created_at__lte = to_date).all()
            elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
                reviews = Review.objects.filter(user=request.user,created_at__gte = from_date, created_at__lte = to_date).all()


            form = ReplyForm()

            return render(request, 'reviews/reviews.html', {'reviews':reviews, 'form':form, 'target':'reviews'})
        # search flags
        elif target == 'flags':
            flags = Flag.objects.filter(created_at__gte = from_date, created_at__lte = to_date).all()
            # admin
            if request.user.is_admin:
                flags = Flag.objects.filter(reported_by__unit=request.user.unit,created_at__gte = from_date, created_at__lte = to_date).all()
            elif request.user.is_customer and not request.user.is_admin and not request.user.is_superuser:
                flags = Flag.objects.filter(user=request.user,created_at__gte = from_date, created_at__lte = to_date).all()

            return render(request, 'flags/allFlags.html', {'flags':flags, 'target':'flags'})

    #if no results
    messages.error(request, 'Something went wrong')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# search a single date
def searchDate(request):
    if request.POST:
        # fetch date
        date = request.POST.get('date')

        # str to datetime instance 
        date = datetime.strptime(date, '%m/%d/%Y')

        # str to datetime instance 
        # date = datetime.strptime('%m/%d/%Y')
        date_1 = date + timedelta(hours=23, minutes=59,seconds = 59, milliseconds=999)

        # filter
        replenishes = FuelReplenish.objects.filter(created_at__gte = date, created_at__lte = date_1).all()

        return render(request, 'replenishments.html', {'replenishes':replenishes, 'target':'replenishes'})


    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# update user roles
@login_required
@admin_or_superuser
def updateRole(request, id):
    if request.POST:
        admin= request.POST.get('admin')
        attendant= request.POST.get('attendant')
        customer= request.POST.get('customer')

        try:
            User.objects.filter(pk=id).update(is_admin= bool(admin), is_attendant= bool(attendant), is_customer= bool(customer))
            
            # for attendant update attendant model
            #addAttendant(request.user.station, User.objects.get(pk=id))
            # print(request.user.station)

            messages.success(request, 'Roles updated successfully.')
        except:
            messages.error(request, 'Something went wrong updating roles.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#add station attendant
# @login_required
# @admin_or_superuser
# def addAttendant(request,stn,usr):
    # stn = Station.objects.get(pk=stn)
    # usr = User.objects.get(pk=userid)
   # Attendant.objects.create(station=stn, user=usr)

    # try:
    #     Attendant.objects.create(station=stn, user=usr)

    #     messages.success(request, 'Attendant successfully added.')
    #     #redirect
    # except:
    #     messages.error(request, 'Something went wrong while adding attendant.')

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# getAttendants
@login_required
@admin_or_superuser
def getAttendants(request):
    attendants = User.objects.filter(is_attendant=True)

    # if admin 
    if request.user.is_admin:
        attendants = User.objects.filter(unit = request.user.unit,is_attendant=True)

    return render(request, 'attendants.html', {'attendants':attendants})












# getAttendants
# @login_required
# @admin_or_superuser
# def delAttendant(request,id):
#     try:
#         Attendant.objects.get(pk=id).delete()
#         messages.success(request, 'Attendant successfully deleted.')
#         #redirect
#     except:
#         messages.error(request, 'Something went wrong.')

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))