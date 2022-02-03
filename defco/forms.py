
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Vehicle

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


