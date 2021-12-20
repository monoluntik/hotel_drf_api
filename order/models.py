from django.db import models

from account.models import MyUser
from main.models import Apartment, Hotel


class Order(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='order')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='apartment')
    email = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=13)    

