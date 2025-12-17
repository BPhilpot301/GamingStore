from django.shortcuts import render
from . import models
from .forms import ContactForm, SignupForm
from django.core.mail import send_mail
import requests
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from catalog.models import Card, Cart, CartItem
from django.shortcuts import redirect, get_object_or_404


# Create your views here.
def home_view(request): 
    all_cards = Card.objects.all()
    return render(request, 'pages/home.html', {"card_list": all_cards})

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
    cart = Cart.objects.filter(user = request.user)
    return render(request, 'pages/cart.html', {"cart": cart})





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
    card = Card.objects.get(id=pk)


    # Get pokemon from the api here
    info = _get_pokemon_info(card.pokemon)

    return render(request, 'pages/details.html', {"card": card, "info": info})



def add_to_cart(request, pk):
    card = Card.objects.get(id=pk)
    user = request.user

    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        card=card
    )

    if not item_created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect("cart")


def cart_view(request):
    cart = request.session.get('cart',[])
    cards = Card.objects.filter(id__in=cart)
    return render(request, 'pages/cart.html',{'cards': cards})


def _recalc_cart_total(cart):
    cart.total = sum(item.card.price * item.quantity for item in cart.cartitem_set.all())
    cart.save()

@login_required
@require_POST
def cart_item_increase(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user, cart__status="open")
    cart_item.quantity += 1
    cart_item.save()
    _recalc_cart_total(cart_item.cart)
    return redirect("cart")

@login_required
@require_POST
def cart_item_decrease(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user, cart__status="open")

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    _recalc_cart_total(cart_item.cart)
    return redirect("cart")


    """
    check if there is a cart for the user
    if not: create one
    if exist get it

    produce a cart object

    create a new CartItem
    pass:
        cart
        cart
    save the cart item

    redirect the user to your new Cart page
    """


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





