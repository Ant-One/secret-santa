from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("draw/new", views.new_draw, name="new_draw")
]