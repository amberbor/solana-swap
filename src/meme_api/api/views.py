import asyncio
from meme_api.app.use_case.buy_job import BuyTradingBot
from meme_api.app.use_case.sell_job import sell
from rest_framework.decorators import api_view
from django.http import JsonResponse


# Create your views here.
@api_view(["GET"])
def buy_job(request):
    bot = BuyTradingBot()
    asyncio.run(bot.run())
    return JsonResponse({"message": "Successful"})

# Create your views here.
@api_view(["GET"])
def sell_job(request):
    a = asyncio.run(sell())
    return JsonResponse({"message": "Successful"})
