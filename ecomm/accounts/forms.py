
from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : "Enter Password",
        'class' :       'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : "Confirm Password",
        'class' :       'form-control'
    }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number','password']
    
    def __init__(self,*args,**kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'PhoneNo.'    
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        email = cleaned_data['email']

        object = Account.objects.filter(email=email)
        if object.exists():
            raise forms.ValidationError("Account Already Exists with this email")

        if len(password) < 8:
            print("Too Short Passowrd")
            raise forms.ValidationError("Password is too Short, It must be 8 Charachters Long")

        if password != confirm_password:
            print("Unmatched Password Exception")
            raise forms.ValidationError("Sorry! Password Didn't Matched.")

