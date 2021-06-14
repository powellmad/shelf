"""Customer order model"""
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.contrib.auth.models import User
from shelfapi.models import Payment

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    payment_type = models.ForeignKey(Payment, on_delete=DO_NOTHING, null=True)
    is_open = models.BooleanField()