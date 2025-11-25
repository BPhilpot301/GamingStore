from django.shortcuts import render
from django.views.generic import ListView
from .models import Card

# Create your views here.
class CardList(ListView):
    model = Card
    template_name = "catalog/list.html"