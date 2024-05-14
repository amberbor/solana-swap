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
    created_at = models.DateTimeField(default=default_datetime)
    updated_at = models.DateTimeField(default=default_datetime)

    class Meta:
        db_table = "coin_info"


class TradePair(models.Model):
    coin = models.ForeignKey(CoinInfo, on_delete=models.PROTECT)
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
    holders = models.IntegerField(null=False, default=2)

    traded = models.BooleanField(default=False)
    txid = models.CharField(max_length=255, null=True)
    txid_url = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(default=default_datetime)
    updated_at = models.DateTimeField(default=default_datetime)

    class Meta:
        db_table = "trade_pair"


class Portofolio(models.Model):

    trade_pair = models.ForeignKey(TradePair, on_delete=models.CASCADE)
    coin = models.ForeignKey(CoinInfo, on_delete=models.CASCADE, default=0)
    amount = models.FloatField(null=True)
    bought_at = models.FloatField(null=True)
    sold_at = models.FloatField(null=True)
    profit = models.FloatField(null=True)
    in_hold = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=default_datetime)
    updated_at = models.DateTimeField(default=default_datetime)

    class Meta:
        db_table = "portfolio"


class Configurations(models.Model):
    solana_wallet_address = models.CharField(
        max_length=300, null=False, blank=False, default="0"
    )
    dev_percentage_min = models.FloatField(default=0)
    dev_percentage_max = models.FloatField(null=False, blank=False)
    current_holders = models.IntegerField(default=2)
    capital_coin = models.FloatField(null=False, blank=False, default=5000)
    amount_to_buy = models.FloatField(null=False, blank=False, default=0.05)
    buy_slippage_rate = models.FloatField(null=False, blank=False, default=10)
    sell_slippage_rate = models.FloatField(null=False, blank=False, default=10)
    expected_profit = models.FloatField(null=False, blank=False, default=2)
    created_at = models.DateTimeField(auto_now_add=True)

    first_wait_seconds = models.IntegerField(null=False, default=60)
    second_wait_seconds = models.IntegerField(null=False, default=30)
    third_wait_seconds = models.IntegerField(null=False, default=15)

    class Meta:
        db_table = "configurations"
