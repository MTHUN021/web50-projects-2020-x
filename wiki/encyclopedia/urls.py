from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("newentry", views.newadd, name="newentry"),
    path("lucky", views.random, name="random_entry"),
    path("search", views.search_entry, name="search"),
    path("wiki/<str:entry>/edit", views.edit, name="editing")
]
