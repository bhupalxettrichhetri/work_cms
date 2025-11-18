# my_app/forms.py
from django import forms
from .models import Organization, ContactPerson, Device,Profile, DevicePassword, Vendor, DeviceConfig, Vpn
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .encrypt_utils import decrypt
from dal import autocomplete


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = [ 'first_name', 'last_name','phone_number', 'email', 'position']  # Ensure these match the model fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
        self.fields['position'].widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
        self.fields['phone_number'].widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
        self.fields['email'].widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})

class OrganizationForm(forms.ModelForm):
    # contact_persons = forms.ModelMultipleChoiceField(
    #     queryset=ContactPerson.objects.all(),
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple
    # )

    class Meta:
        model = Organization
        fields = ['name', 'address', 'email']
        labels = {
            'name': 'Organization Name',
            'address': 'Organization Address',
            'email': 'Organization Email',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
        self.fields['address'].widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
        self.fields['email'].widget = forms.EmailInput(attrs={'type': 'email', 'class': 'form-control'})

# ContactPersonFormSet = inlineformset_factory(
#     Organization,
#     ContactPerson,
#     form=ContactPersonForm,
#     extra=1,
#     # can_delete=True
# )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','username']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'profile_picture']




class DeviceForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(error_messages={'required': 'Agency type required'},
                                                #  label= "Agency Type",
                                                 queryset=Vendor.objects.all(),
                                                 required=True,
                                                 widget=autocomplete.ModelSelect2(url='dashboard:vendor-autocomplete',
                                                                                          attrs={
                                                                                              'class': 'form-control p-0 border-0',
                                                                                              'data-placeholder': 'Choose agency Name'
                                                                                          })
                                                )
    class Meta:
        model = Device
        fields = ['name', 'ip_address', 'vendor', 'firmware_version']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
        self.fields['ip_address'].widget = forms.TextInput(attrs={'type': 'text', 'class': 'form-control'})
        self.fields['firmware_version'].widget = forms.EmailInput(attrs={'type': 'text', 'class': 'form-control'})


class DevicePasswordForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password if changing','type': 'text', 'class': 'form-control'}),
        required=False
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'type': 'text', 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = DevicePassword
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(DevicePasswordForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.pk:
            # Decrypt the password and set it as the initial value
            decrypted_password = decrypt(instance.password)
            self.fields['password'].initial = decrypted_password
   


class DeviceConfigForm(forms.ModelForm):
    class Meta:
        model = DeviceConfig
        fields = ['config_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['config_file'].widget = forms.TextInput(attrs={'type': 'file', 'class': 'form-control'})
        self.fields['config_file'].required = False

class VpnForm(forms.ModelForm):
    class Meta:
        model = Vpn
        fields = ['ip_address', 'username', 'password','port','organization']
        widgets = {
            'ip_address': forms.TextInput(attrs={
                'placeholder': 'Enter IP address',
                'type': 'text',
                'class': 'form-control',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter IP address',
                'type': 'text',
                'class': 'form-control',
            }),
            'password': forms.TextInput(attrs={
                'placeholder': 'Enter IP address',
                'type': 'text',
                'class': 'form-control',
            }),
            'organization': forms.Select(attrs={
                'class': 'form-control',
            }),
            'port': forms.NumberInput(attrs={
                'placeholder': 'Enter IP address',
                'class': 'form-control',
            }),
         }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VpnForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['organization'].queryset = Organization.objects.filter(created_by=user)
        self.fields['organization'].empty_label = "------"


        