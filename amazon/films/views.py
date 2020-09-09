from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# Create your views here.
movies = []

class NewMovieForm(forms.Form):
    movie = forms.CharField(label="New Movie")
    #release = forms.IntegerField(label="YEAR", min_value=1960, max_value=2020)


def add(request):
    if request.method == "POST":
        form = NewMovieForm(request.POST)
        if form.is_valid():
           movie =  form.cleaned_data["movie"]
           request.session["movies"] += [movie]
           return HttpResponseRedirect(reverse("films:index"))
        else:
            return render(request, "films/add.html", {
                "form": form
            })


    return render(request, "films/add.html", {
        "form": NewMovieForm()
    })


def index(request):
    if "movies" not in request.session:
        request.session["movies"] = []

    return render(request, "films/list.html", {
        "movies": request.session["movies"]
    })