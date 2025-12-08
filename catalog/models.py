from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Card(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="cards/", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    pokemon = models.CharField(max_length=50)
    type = models.CharField(max_length=75)
    weakness = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    set = models.CharField(max_length=200)
    health = models.IntegerField()
    


    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    
