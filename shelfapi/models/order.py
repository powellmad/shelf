"""Customer order model"""
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.contrib.auth.models import User
from shelfapi.models import Payment, Shipping

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    payment_type = models.ForeignKey(Payment, on_delete=DO_NOTHING, null=True)
    shipping = models.ForeignKey(Shipping, on_delete=DO_NOTHING, null=True)
    is_open = models.BooleanField()
    products = models.ManyToManyField('Product', through= 'OrderProduct')