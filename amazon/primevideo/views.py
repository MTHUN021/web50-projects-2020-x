from django.shortcuts import render
from django.http import HttpResponse

users = ['MITHUN', 'GAURAV', 'SHARATH']
# Create your views here.

def index(request):
    return HttpResponse("Welcome to Prime video")

def default(request, x):
    return render(request, "primevideo/sign.html", {
        "x": x
    })

def show(request):
    return render(request, 'primevideo/show.html', {
        "users": users
    })