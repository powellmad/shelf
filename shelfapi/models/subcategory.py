from django.db import models
from django.db.models.deletion import CASCADE

class Subcategory(models.Model):
    label = models.CharField(max_length=50)
    category = models.ForeignKey("Category", on_delete=CASCADE)
