from django.db import models


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

