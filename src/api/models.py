from django.db import models
from datetime import datetime

def default_datetime():
    return datetime.now()
# Create your models here.
class Coins(models.Model):
    message_id = models.IntegerField(unique=True, null=False, blank=False)
    mint_address = models.CharField(max_length=300, unique=True)
    name = models.CharField(max_length=250)
    symbol = models.CharField(max_length=250)
    creator = models.CharField(max_length=250, null=True)
    cap = models.FloatField(max_length=250)
    dev_percentage = models.FloatField(default=0)
    bought = models.FloatField(max_length=250)
    created_at = models.DateTimeField(default=default_datetime)


class Configurations(models.Model):
    dev_percentage_min = models.FloatField(default=0)
    dev_percentage_max = models.FloatField(null=False, blank=False)
    current_holders = models.IntegerField(default=2)
    capital_coin = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

