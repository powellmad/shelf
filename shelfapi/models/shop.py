"""Seller's Shop model"""
from shelfapi.models.category import Category
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.contrib.auth.models import User
from shelfapi.models import Category

class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    category = models.ForeignKey(Category, on_delete=DO_NOTHING)
    name = models.CharField(max_length=50)
    logo_path = models.URLField()