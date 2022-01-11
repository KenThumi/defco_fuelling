
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

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

class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField()
    rank =   forms.CharField( widget=forms.Select(choices=ranks))
    svc_id_img = forms.FileField( label='Upload copy of your Job ID')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['svc_no'].widget.attrs.update({
            'required':'',
            'name':'svc_no',
            'type':'text',
            'class':'form-control',
            'placeholder':'Service No.',
        })

        self.fields['rank'].widget.attrs.update({
            'required':'',
            'name':'rank',
            'type':'select',
            'class':'form-control',
            'placeholder':'Rank',
        })

        self.fields['name'].widget.attrs.update({
            'required':'',
            'name':'name',
            'type':'text',
            'class':'form-control',
            'placeholder':'Name',
        })

        self.fields['unit'].widget.attrs.update({
            'required':'',
            'name':'unit',
            'type':'text',
            'class':'form-control',
            'placeholder':'Enter your Unit',
        })

        self.fields['mobile'].widget.attrs.update({
            'required':'',
            'name':'mobile',
            'type':'text',
            'class':'form-control',
            'placeholder':'Phone No.',
        })

        self.fields['email'].widget.attrs.update({
            'required':'',
            'name':'email',
            'type':'email',
            'class':'form-control',
            'placeholder':'Enter your Email',
        })

        self.fields['svc_id_img'].widget.attrs.update({
            'required':'',
            'name':'svc_id_img',
            'type':'file',
            'class':'form-control',
            'placeholder':'Service ID Copy',
        })

        self.fields['password1'].widget.attrs.update({
            'required':'',
            'name':'password1',
            'type':'password',
            'class':'form-control',
            'placeholder':'Password',
        })

        self.fields['password2'].widget.attrs.update({
            'required':'',
            'name':'password2',
            'type':'password',
            'class':'form-control',
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
        fields = ['svc_no','rank','name','unit','mobile','email','svc_id_img','password1','password2']
        icons = { 
                  'password1':'lock',
                  'password2':'lock', 
                  'svc_no':'user',
                  'mobile':'phone',
                  'rank':'user-tie',
                  'svc_id_img':'id-card',
                  'name':'user-circle',
                  'unit':'users',
                  'email':'envelope'
                }