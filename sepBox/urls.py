from django.urls import path
from .views import calcSeparator

urlpatterns = [
path('',calcSeparator,name='calcSep')
]