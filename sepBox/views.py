from django.shortcuts import render

# Create your views here.

def calcSeparator(request):
    return render(request,'main.html')
