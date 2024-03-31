from django.shortcuts import render, redirect
from .forms import RegistrationForm, ContactForm, AppointmentForm
from django.contrib.auth import login, logout, authenticate
# Create your views here.
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
import os
from dotenv import load_dotenv

from .graphgen import generate_graph

load_dotenv()
password = os.getenv("MONGO_PASS")  #hide before push
user = os.getenv("MONGO_USER")

uri = f"mongodb+srv://{user}:{password}@cluster0.biqo3x8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
hospitaldb = client['hospital_data']
enquirycol = hospitaldb['enquiries']
appointmentcol = hospitaldb['appointments']

import vonage
key = os.getenv("VONAGE_KEY")
secret = os.getenv("VONAGE_SECRET")
client = vonage.Client(key=key, secret=secret)  ### Remove Key & Secret Before Pushing to GitHub
sms = vonage.Sms(client)



def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            number = form.cleaned_data['number']
            message = form.cleaned_data['message']
            
            enquiry = {
                "name": name,
                "email": email,
                "number": number,
                "subject": subject,
                "message": message,
                "date": datetime.datetime.now()
            }
            x = enquirycol.insert_one(enquiry)
            print(name, email, subject, number, message,x)
            text = f"{name}, your enquiry for '{subject}' has been recieved and will be processed soon. Thank you for contacting us. "
            responseData = sms.send_message(
            {
                "from": "MediEase",
                "to": number,
                "text": text,
            }
            )

            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")
            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

            return render(request, 'main/contact.html', {'form': form, 'contact': True})
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form, 'contact': False})   

def privacy(request):
    return render(request, 'main/privacy.html')

def terms(request):
    return render(request, 'main/terms.html')

def summary(request):
    generate_graph()
    return render(request, 'main/graph.html')

def gallery(request):
    return render(request, 'main/gallery.html')

def doctors(request):
    return render(request, 'main/doctors.html')

def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['number']
            purpose = form.cleaned_data['subject']
            date = form.cleaned_data['date']
            time = form.cleaned_data['Time']
            department = form.cleaned_data['Department']

            appointment = {
                "name": name,
                "email": email,
                "phone": phone,
                "purpose": purpose,
                "date": str(date),
                "time": time,
                "department": department,
                "status": "Pending",
                "date_time": datetime.datetime.now()
            }
            x = appointmentcol.insert_one(appointment)
            print(name, email, phone, purpose, date, time, department, x.inserted_id)
            
            text = f"{name}, your appointment for '{purpose}' on {date} at {time} has been booked. Thank you for choosing MediEase."
            for i in range(2):
                responseData = sms.send_message(
                {
                    "from": "MediEase",
                    "to": phone,
                    "text": text,
                }
                )

                if responseData["messages"][0]["status"] == "0":
                    print("Message sent successfully.")
                else:
                    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

            return render(request, 'main/appointment.html', {'form': form, 'appointment': True})
        else:
            print(form.errors)

    else:
        form = AppointmentForm()
    return render(request, 'main/appointment.html', {'form': form, 'appointment': False})



def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/sign_up.html', {'form': form})