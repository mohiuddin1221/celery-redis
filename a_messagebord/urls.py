from django.urls import path, include
from .views import *

urlpatterns = [
    path('', messagebord_view, name = 'messagebord-view'),
    path('subscribe/', subscribe, name = 'subscribe'),
]
