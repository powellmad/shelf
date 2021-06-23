"""Shipping Info model"""
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.contrib.auth.models import User

class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    phone = models.IntegerField()