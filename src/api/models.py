from django.db import models
from datetime import datetime

def default_datetime():
    return datetime.now()
# Create your models here.
class CoinInfo(models.Model):
    message_id = models.IntegerField(unique=True, null=False, blank=False)
    mint_address = models.CharField(max_length=300, unique=True)
    name = models.CharField(max_length=250)
    symbol = models.CharField(max_length=250)
    creator = models.CharField(max_length=250, null=True)
    cap = models.FloatField(max_length=250)
    dev_percentage = models.FloatField(default=0)
    bought = models.FloatField(max_length=250)
    created_at = models.DateTimeField(default=default_datetime)

    class Meta:
        db_table = 'coin_info'

class TradePair(models.Model):
    coin_id = models.ForeignKey(CoinInfo, on_delete=models.PROTECT)
    base_coin_amount = models.FloatField()
    coin_amount = models.FloatField()
    min_amount_out = models.FloatField(null=True, blank=True)
    current_price = models.FloatField(null=True, blank=True)
    execution_price = models.FloatField(null=True, blank=True)
    price_impact = models.FloatField(null=True, blank=True)
    is_pump_fun = models.BooleanField(default=True)
    platform_fee = models.FloatField()
    base_currency = models.CharField(max_length=250)
    quote_currency = models.CharField(max_length=250)

    class Meta:
        db_table = 'trade_pair'
class Portofolio(models.Model):
    txid = models.CharField(unique=True, blank=False, null=False)
    txid_url = models.CharField(unique=True, max_length=500)
    trade_pair = models.ForeignKey(TradePair, on_delete=models.PROTECT)
    amount = models.FloatField(null=False, blank=False)
    base_amount = models.FloatField()

    class Meta:
        db_table = 'portfolio'


class Configurations(models.Model):
    dev_percentage_min = models.FloatField(default=0)
    dev_percentage_max = models.FloatField(null=False, blank=False)
    current_holders = models.IntegerField(default=2)
    capital_coin = models.FloatField(null=False, blank=False, default=5000)
    amount_to_buy = models.FloatField(null=False, blank=False, default=0.05)
    slippage_rate = models.FloatField(null=False, blank=False, default=10)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'configurations'