from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="payment_types")
    merchant_name = models.CharField(max_length=25,)
    account_number = models.CharField(max_length=25)
    expiration_date = models.DateField(default="0000-00-00",)