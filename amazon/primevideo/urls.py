from django.contrib import admin

from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("users", views.show, name="users"),
    path("<str:x>", views.default, name="default")
]