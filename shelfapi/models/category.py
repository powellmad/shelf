from django.db import models

class Category(models.Model):
    label=models.CharField(max_length=50)
    image_path=models.URLField(null=True)