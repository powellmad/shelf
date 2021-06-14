"""Shipping Info model"""
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.contrib.auth.models import User
from shelfapi.models import Order

class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    order = models.ForeignKey(Order, on_delete=DO_NOTHING)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.IntegerField(max_length=10)
    phone = models.IntegerField(max_length=10)