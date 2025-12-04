from django.shortcuts import render
from . import models
from .forms import ContactForm, SignupForm
from django.core.mail import send_mail
import requests
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView


DATA = [
    {
        "id": 1,
        "name" : "Special Delivery Charizard",
        "price": 135.28,
        "pokemon": "Charizard",
        "image": "img/Charizard.jpg",
        "set": "Sword & Shield Promo Cards",
        "type": "Fire, Flying",
        "weakness": "Rock, Water, and Electric types",
        "health": "160HP"
        
    },
     {
        "id": 2,
        "name" : "Lt. Surge",
        "price": 3.83,
        "pokemon": "Lt. Surge",
        "image": "img/Brock.jpg",
        "set": "Gym Heros",
        "type": "Trainer",
        "weakness": "None",
        "health": "0HP"
    },
     {
        "id": 3,
        "name" : "Mew Alt Art",
        "price": 135.58,
        "pokemon": "Mew",
        "image": "img/mew.jpg",
        "set": "Scarlet & Violet—151",
        "type": "Psychic",
        "weakness": "Bug, Dark, and Ghost-type",
        "health": "180HP"
    },
    {
        "id": 4,
        "name" : "Mew Full Art",
        "price": 133.55,
        "pokemon": "Mew",
        "image": "img/mewfull.jpg",
        "set": "Scarlet & Violet—151",
        "type": "Psychic",
        "weakness": "Bug, Dark, and Ghost-type",
        "health": "180HP"
    },
    {
        "id": 5,
        "name" : "Ninetales",
        "price": 114.40,
        "pokemon": "Ninetales",
        "image": "img/ninetales.jpg",
        "set": "Japanese Base Set",
        "type": "Fire",
        "weakness": "Rock, Water, and Ground types",
        "health": "60HP"
    },
    {
        "id": 6,
        "name" : "Mewtwo",
        "price": 244.85,
        "pokemon": "Mewtwo",
        "image": "img/mewtwoJP.jpg",
        "set": "Sword & Shield Promo Cards",
        "type": "Psychic",
        "weakness": "Bug, Dark, and Ghost-type",
        "health": "170HP"
    },
    {
        "id": 7,
        "name" : "Mew Gold Full Art",
        "price": 142.97,
        "pokemon": "Mew",
        "image": "img/mewgold.jpg",
        "set": "Scarlet & Violet—151",
        "type": "Psychic",
        "weakness": "Bug, Dark, and Ghost-type",
        "health": "180HP"
    },
    {
        "id": 8,
        "name" : "Mew Shiny Full Art",
        "price": 223.76,
        "pokemon": "Mew",
        "image": "img/mewshiny.jpg",
        "set": "Scarlet & Violet—151",
        "type": "Psychic",
        "weakness": "Bug, Dark, and Ghost-type",
        "health": "180HP"
    },
    {
        "id": 9,
        "name" : "Pikachu and Friends",
        "price": 183.27,
        "pokemon": "Pikachu",
        "image": "img/pikachu2.jpg",
        "set": "Scarlet & Violet-Paldean Fates",
        "type": "Electric",
        "weakness": "Ground-type",
        "health": "60HP"
    },
    {
        "id": 10,
        "name" : "Pikachu Alt Art",
        "price": 358.00,
        "pokemon": "Pikachu",
        "image": "img/pikacity.jpg",
        "set": "Scarlet & Violet—151",
        "type": "Electric",
        "weakness": "Ground-type",
        "health": "60HP"
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

def login_view(request):
    return render(request, 'pages/login.html')

def create_view(request):
    return render(request, 'pages/create.html')

def cart_view(request):
    return render(request, 'pages/cart.html', {"card_list": DATA})

class UserLogin(LoginView):
    template_name = 'pages/login.html'

    def get_success_url(self):
        return reverse('home')

def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

class UserSignup(CreateView):
    template_name = "pages/create.html"
    success_url = reverse_lazy("login")
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save

        return super().form_valid(form)


#class UserCreate(CreateView):
    #template_name = "users/create.html"

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


