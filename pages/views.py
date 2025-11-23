from django.shortcuts import render
from . import models
from .forms import ContactForm
from django.core.mail import send_mail
import requests

DATA = [
    {
        "id": 1,
        "name" : "Special Delivery Charizard",
        "price": 135.28,
        "pokemon": "Charizard",
        "image": "img/Charizard.jpg",
    },
     {
        "id": 2,
        "name" : "Lt. Surge",
        "price": 3.83,
        "pokemon": "Lt. Surge",
        "image": "img/Brock.jpg"
    },
     {
        "id": 3,
        "name" : "Mew Alt Art",
        "price": 135.58,
        "pokemon": "Mew",
        "image": "img/mew.jpg"
    },
    {
        "id": 4,
        "name" : "Mew Full Art",
        "price": 0,
        "pokemon": "Mew",
        "image": "img/mewfull.jpg"
    },
    {
        "id": 5,
        "name" : "Ninetails",
        "price": 114.40,
        "pokemon": "Ninetails",
        "image": "img/ninetails.jpg"
    },
    {
        "id": 6,
        "name" : "Mewtwo",
        "price": 244.85,
        "pokemon": "Mewtwo",
        "image": "img/mewtwoJP.jpg"
    },
    {
        "id": 7,
        "name" : "Mew Gold Full Art",
        "price": 142.97,
        "pokemon": "Mew",
        "image": "img/mewgold.jpg"
    },
    {
        "id": 8,
        "name" : "Mew Shiny Full Art",
        "price": 223.76,
        "pokemon": "Mew",
        "image": "img/mewshiny.jpg"
    },
    {
        "id": 9,
        "name" : "Pikachu and Friends",
        "price": 183.27,
        "pokemon": "Pikachu",
        "image": "img/pikachu2.jpg"
    },
    {
        "id": 10,
        "name" : "Pikachu Alt Art",
        "price": 358.00,
        "pokemon": "Pikachu",
        "image": "img/pikacity.jpg"
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

def details_view(request, pk):    
    selected_card = {}
    for card in DATA:
        if card["id"] == pk:
            # found the one
            selected_card = card
            break # stop looking

    # Get pokemon from the api here
    info = _get_pokemon_info(card["pokemon"])

    return render(request, 'pages/details.html', {"card": selected_card, "info": info})

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
    



def _get_pokemon_info(name):
    # wil call the api to read the information about the pokemon
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)

    if response.ok:
        data = response.json()
        return data
    else:
        print(f"Error {response.status_code}")
        print(response.text)