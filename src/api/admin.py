from django.contrib import admin
from api.models import CoinInfo, Configurations

# Register your models here.
admin.site.register(CoinInfo)
admin.site.register(Configurations)