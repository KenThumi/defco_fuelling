from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import fields
# from django.http import request
from .models import FuelReplenish, Price, Reply, Review, Station, Transaction, User, Vehicle
from django_select2 import forms as s2forms

# input select  choices
ranks = [
    ('','-select-'),
    ('Gen','General'),
    ('Lt Gen', 'Lt Gen'),
    ('Maj Gen','Maj Gen'),
    ('Brig','Brig'),
    ('Col','Col'),
    ('Lt Col','Lt Col'),
    ('Maj','Maj'),
    ('Capt','Capt'),
    ('Lt', 'Lt'),
    ('2Lt','2Lt'),
    ('Wo1','Wo1'),
    ('Wo2','Wo2'),
    ('Ssgt','Ssgt'),
    ('Sgt','Sgt'),
    ('Cpl','Cpl'),
    ('L/Cpl','LCpl'),
    ('Spte','Spte'),
    ('Pte','Pte'),
    ('Civ','Civ')
]

vehicle_makes = [
            ('','-select-'),
            ('Toyota','Toyota'),
            ('Nissan','Nissan'),
            ('Honda','Honda'),
            ('Mitsubishi','Mitsubishi'),
            ('Mercedes-Benz','Mercedes-Benz'),
            ('BMW','BMW'),
            ('Mazda','Mazda'),
            ('Subaru','Subaru'),
            ('Volkswagen','Volkswagen'),
            ('Suzuki','Suzuki'),
            ('Land Rover','Land Rover'),
            ('Isuzu','Isuzu'),
            ('Audi','Audi'),
            ('Ford','Ford'),
            ('Daihatsu','Daihatsu'),
            ('Lexus','Lexus'),
            ('Motorbike','Motorbike'),
            ('Other','Other')
        ]

modes = [
    ('Cash','Cash'),
    ('MPESA','MPESA'),
    ('Bank ATM','Bank ATM')
]

review_types = [
    ('','- select -'),
    ('complaint','Complaint'),
    ('comment','Comment'),
    ('recommendation','Recommendation')
]

product_types = [
    ('','- select -'),
    ('petroleum','Petroleum'),
    ('diesel','Diesel')
]

class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField()
    rank =   forms.CharField( widget=forms.Select(choices=ranks))
    image = forms.FileField( label='Upload copy of your Job ID')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['svc_no'].widget.attrs.update({
            'required':'',
            'name':'svc_no',
            'type':'text',
            'class':'form-control form-control-sm',
            'placeholder':'Service No.',
        })

        self.fields['rank'].widget.attrs.update({
            'required':'',
            'name':'rank',
            'type':'select',
            'class':'form-control form-control-sm',
            'placeholder':'Rank',
        })

        self.fields['name'].widget.attrs.update({
            'required':'',
            'name':'name',
            'type':'text',
            'class':'form-control form-control-sm',
            'placeholder':'Name',
        })

        self.fields['username'].widget.attrs.update({
            'required':'',
            'name':'username',
            'type':'text',
            'class':'form-control form-control-sm',
            'placeholder':'Username',
        })

        self.fields['unit'].widget.attrs.update({
            'required':'',
            'name':'unit',
            'type':'text',
            'class':'form-control form-control-sm',
            'placeholder':'Enter your Unit',
        })

        self.fields['mobile'].widget.attrs.update({
            'required':'',
            'name':'mobile',
            'type':'text',
            'class':'form-control form-control-sm',
            'placeholder':'Phone No.',
        })

        self.fields['email'].widget.attrs.update({
            'required':'',
            'name':'email',
            'type':'email',
            'class':'form-control form-control-sm',
            'placeholder':'Enter your Email',
        })

        self.fields['image'].widget.attrs.update({
            'name':'image',
            'type':'file',
            'class':'form-control form-control-sm',
            # 'required':'False'
        })

        self.fields['password1'].widget.attrs.update({
            'required':'',
            'name':'password1',
            'type':'password',
            'class':'form-control form-control-sm',
            'placeholder':'Password',
        })

        self.fields['password2'].widget.attrs.update({
            'required':'',
            'name':'password2',
            'type':'password',
            'class':'form-control form-control-sm',
            'placeholder':'Retype Password',
        })

        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            # add form-control class to all fields
            # field.widget.attrs['class'] = 'form-control'
            # set icon attr on field object
            if field_name in icons:
                field.icon = icons[field_name]

        

    class Meta:
        model = User
        fields = ['svc_no','rank','name','unit','username','email','mobile','image','password1','password2']
        icons = { 
                  'password1':'lock',
                  'password2':'lock', 
                  'svc_no':'user',
                  'mobile':'phone',
                  'rank':'user-tie',
                  'image':'id-card',
                  'name':'user-circle',
                  'username':'user-circle',
                  'unit':'users',
                  'email':'envelope'
                }


class ProfileEditForm(UserRegisterForm):
    image = forms.FileField(required=False)


class VehicleForm(forms.ModelForm):
    make =   forms.CharField( widget=forms.Select(choices=vehicle_makes))
    image = forms.FileField( label='Upload vehicle image')
    logbook = forms.FileField( label='Upload logbook image or scanned documents proving vehicle ownership')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['reg_no'].widget.attrs.update({
            'required':'',
            'name':'reg_no',
            'type':'text',
            'class':'form-control form-control-sm',
            'placeholder':'e.g., KCC 123K',
        })

        self.fields['make'].widget.attrs.update({
            'required':'',
            'name':'make',
            'type':'select',
            'class':'form-control form-control-sm',
        })

        self.fields['model'].widget.attrs.update({
            'required':'',
            'name':'model',
            'type':'text',
            'class':'form-control form-control-sm',
            'placeholder':'Vehicle Model',
        })

        self.fields['logbook_no'].widget.attrs.update({
            'required':'',
            'name':'logbook_no',
            'type':'text',
            'class':'form-control form-control-sm',
            'placeholder':'Logbook No.',
        })

        self.fields['image'].widget.attrs.update({
            'name':'image',
            'type':'file',
            'class':'form-control form-control-sm',
        })

        self.fields['logbook'].widget.attrs.update({
            'name':'logbook',
            'type':'file',
            'class':'form-control form-control-sm',
        })


        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]


    class Meta:
        model = Vehicle
        fields = ['reg_no','make','model','image','logbook_no','logbook']
        icons = { 
                  'reg_no':'registered',
                  'make':'car', 
                  'model':'car',
                  'image':'car',
                  'logbook_no':'car',
                  'logbook':'file-alt',
                }


class EditVehicleForm(VehicleForm):
    image = forms.FileField( required=False )
    logbook = forms.FileField( required=False)



class StationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['admin'].queryset = User.objects.filter(is_admin=True)
   
        self.fields['name'].widget.attrs.update({
            'required':'',
            'name':'name',
            'type':'text',
            'class':'form-control form-control-sm',
            'placeholder':'Station name',
        })

        self.fields['admin'].widget.attrs.update({
            'required':'',
            'name':'admin',
            'type':'select',
            'class':'form-control form-control-sm',
        })

        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]


    class Meta:
        model = Station
        exclude = ['open']
        icons = { 
                  'name':'gas-pump',
                  'admin':'user', 
                }


class ReplenishForm(forms.ModelForm):
    # current_amount=forms.IntegerField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['admin'].queryset = User.objects.filter(is_admin=True)
   
        self.fields['station'].widget.attrs.update({
            'required':'',
            'name':'station',
            'type':'select',
            'class':'form-control form-control-sm',
        })

        self.fields['replenished_amount'].widget.attrs.update({
            'required':'',
            'name':'replenished_amount',
            'type':'number',
            'class':'form-control form-control-sm',
            'placeholder':'Replenish Amount in Litres',
        })


        self.fields['batch_no'].widget.attrs.update({
            'required':'',
            'name':'batch_no',
            'type':'text',
            'class':'form-control form-control-sm',
            'placeholder':'Batch No.',
        })


        self.fields['supplier'].widget.attrs.update({
            'required':'',
            'name':'supplier',
            'type':'select',
            'class':'form-control form-control-sm',
            'placeholder':'Supplier',
        })

        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]


    class Meta:
        model = FuelReplenish
        exclude = ['current_amount']
        # fields = '__all__'
        icons = { 
                  'station':'gas-pump',
                  'replenished_amount':'fill-drip', 
                  'batch_no':'clipboard-list',
                  'supplier':'user-tie'
                }


class VehicleWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "reg_no__icontains",
    ]


class TransactionForm(forms.ModelForm):
    payment_mode =    forms.CharField( widget=forms.Select(choices=modes))
    amount =  forms.IntegerField( label='Amount (Ksh)')
    

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        # self.fields['batch_no'].queryset = User.objects.filter(is_admin=True)

        self.fields['batch_no'].queryset = FuelReplenish.objects.filter(station=self.user.station)
   
        self.fields['vehicle'].widget.attrs.update({
            'required':'',
            'name':'vehicle',
            'type':'select',
            'class':'form-control form-control-sm',
        })

        self.fields['litres'].widget.attrs.update({
            'required':'',
            'name':'litres',
            'type':'number',
            'class':'form-control form-control-sm',
        })

        self.fields['amount'].widget.attrs.update({
            'required':'',
            'name':'amount',
            'type':'number',
            'class':'form-control form-control-sm',
        })

        self.fields['payment_mode'].widget.attrs.update({
            'required':'',
            'name':'payment_mode',
            'type':'text',
            'class':'form-control form-control-sm',

        })
        
        self.fields['station'].widget.attrs.update({
            'required':'',
            'name':'station',
            'type':'select',
            'disabled':True,
            'class':'form-control form-control-sm',
        })

        self.fields['batch_no'].widget.attrs.update({
            'required':'',
            'name':'batch_no',
            'type':'select',
            'class':'form-control form-control-sm',
        })

        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]


    class Meta:
        model = Transaction
        exclude = ['attendant','date']
        widgets = {
            "vehicle": VehicleWidget,
           
        }
        icons={ 
                'vehicle':'car',
                'litres':'fill-drip',
                'amount':'dollar-sign',
                'payment_mode':'money-bill',
                'station':'gas-pump',
                'batch_no':'clipboard-list',
              }
            

class ReviewForm(forms.ModelForm):
    review_type =    forms.CharField( widget=forms.Select(choices=review_types))
    description = forms.CharField(widget=forms.Textarea())
    reveal_id =  forms.BooleanField( label='Select to Reveal Identity')
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['batch_no'].queryset = FuelReplenish.objects.filter(station=self.user.station)
   
        self.fields['review_type'].widget.attrs.update({
            'required':'',
            'name':'review_type',
            'type':'select',
            'class':'form-control form-control-sm',
        })

        self.fields['description'].widget.attrs.update({
            'required':'',
            'name':'description',
            'type':'textarea',
            'class':'form-control form-control-sm',
        })

        
        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]


    class Meta:
        model = Review
        fields = ['review_type','description', 'reveal_id']
        
        icons={ 
                'review_type':'comments',
                'description':'pen'
              }


class ReplyForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(), label='Reply')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['batch_no'].queryset = FuelReplenish.objects.filter(station=self.user.station)
   
        self.fields['description'].widget.attrs.update({
            'required':'',
            'name':'description',
            'class':'form-control form-control-sm',
            'rows':2
            
        })
    
    class Meta:
        model = Reply
        fields = ['description']



class PriceForm(forms.ModelForm):
    price = forms.CharField(label='Price per Litre (KSH)')
    type = forms.CharField( widget=forms.Select(choices=product_types))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['batch_no'].queryset = FuelReplenish.objects.filter(station=self.user.station)
   
        self.fields['type'].widget.attrs.update({
            'required':'',
            'name':'description',
            'class':'form-control form-control-sm',            
        })

        self.fields['price'].widget.attrs.update({
            'required':'',
            'name':'description',
            'class':'form-control form-control-sm',            
        })

        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]
    
    class Meta:
        model = Price
        fields = ['type', 'price']

        icons = { 
                  'type':'gas-pump',
                  'price':'coins', 
                }