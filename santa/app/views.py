from django.shortcuts import render
from django.template import loader

# Create your views here.

def index(request):
    return render(request, "index.html")

def new_draw(request):
    return render(request, "new_draw.html")