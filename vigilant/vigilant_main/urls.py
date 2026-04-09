from django.contrib import admin
from django.urls import path

from . import views

app_name = 'vigilant_main'

urlpatterns = [
    path('', views.main, name="main"),
    path('connection', views.connection, name="connection"),
]
