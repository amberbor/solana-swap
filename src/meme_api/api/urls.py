from django.contrib import admin
from django.urls import path
from . import views

# from . import views
urlpatterns = [
    path('buy/', views.buy_job),
    path('sell/', views.sell_job),
]
