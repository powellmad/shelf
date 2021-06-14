from django.db import models
from django.db.models.deletion import DO_NOTHING
from shelfapi.models import Order, Product

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=DO_NOTHING)