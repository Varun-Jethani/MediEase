from django import forms 
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="First Name", max_length=100, required=True)
    last_name = forms.CharField(label="Last Name", max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']


class ContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    subject = forms.CharField(label="Subject", max_length=100, required=True)
    number= forms.CharField(label="Phone", max_length=100, required=True)
    message = forms.CharField(label="Message", widget=forms.Textarea, required=True)

    class Meta:
        fields = ['name','email','subject','number','message']

class AppointmentForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    subject = forms.CharField(label="Subject", max_length=100, required=True)
    number = forms.CharField(label="Number", max_length=100, required=True)
    Department = forms.CharField(label="Department", max_length=100, required=True)
    date = forms.DateField(label="Date", required=True)
    Time = forms.CharField(label="Time", required=True)
    

    class Meta:
        fields = ['name','email','subject','number','Department','date','Time']