from django.urls import path
from . import views

urlpatterns = [
    path('', views.calc_separator, name='calc_separator'),
]
