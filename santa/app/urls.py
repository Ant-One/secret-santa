from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("draw/new", views.new_draw, name="new_draw"),
    path("draw/create", views.create_draw, name="create_draw"),
    path("draw/<int:draw_id>/", views.draw_details, name="draw_details"),
    path("draw/<int:draw_id>/edit", views.draw_edit, name="draw_edit"),
]