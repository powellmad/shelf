from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from shelfapi.models import Shop, Type
from django.contrib.auth.models import User

class Product(models.Model): 
    name = models.CharField(max_length=50)
    image_path = models.URLField()
    quantity = models.IntegerField()
    description = models.TextField()
    price = models.IntegerField()
    subcategory = models.ForeignKey(Type, on_delete=DO_NOTHING)
    shop = models.ForeignKey(Shop, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)