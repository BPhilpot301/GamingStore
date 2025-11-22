from django.shortcuts import render
from . import models
from .forms import ContactForm
from django.core.mail import send_mail

DATA = [
    {
        "id": 1,
        "name" : "",
        "price": 0,
        "pokemon": "",
        "image": "img/Charizard.jpg"
    },
     {
        "id": 1,
        "name" : "",
        "price": 0,
        "pokemon": "",
        "image": ""
    },
     {
        "id": 1,
        "name" : "",
        "price": 0,
        "pokemon": "",
        "image": ""
    },

]

# Create your views here.
def home_view(request):
    return render(request, 'pages/home.html', {"card_list": DATA})

def about_view(request):
    return render(request, 'pages/about.html')

def contact_view(request):
    return render(request, 'pages/contact.html')

def tourn_view(request):
    return render(request, 'pages/tourn.html')

def details_view(request):
    return render(request, 'pages/details.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            message_body =(
                f'You have any questions, feel free to message me!'
                f'Name: {name}\n'
                f'Email: {email}\n'
                f'Message: {message}\n'
                )

            try:
                send_mail(
                    "Email from The Card Shop",
                    message_body,
                    email,
                    ['britphilpot43@gmail.com']
                )
                print("Email was sent")    
                form = ContactForm()
                return render(request, 'pages/contact.html', {'form':form})
            except Exception as e:
                print(f'Error sending email: {e}')
                return render(request, 'pages/contact.html', {'form':form})

        else:
                print("Invalid data")
    else:
        form = ContactForm()
        return render(request, 'pages/contact.html', {'form':form})