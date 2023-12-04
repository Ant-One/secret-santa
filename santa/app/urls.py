from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("draw/new", views.new_draw, name="new_draw"),
    path("draw/create", views.create_draw, name="create_draw"),
    path("draw/<int:draw_id>/", views.draw_details, name="draw_details"),
    path("draw/<int:draw_id>/edit", views.draw_edit, name="draw_edit"),
    path("draw/<int:draw_id>/do_draw", views.do_draw, name="do_draw"),
    path("draw/<int:draw_id>/p/<int:participant_id>", views.participant_draw, name="participant_draw"),
    path("draw/<int:draw_id>/share_link", views.share_link, name="share_link"),
    path("draw/<int:draw_id>/pairing/<int:pairing_id>", views.show_pairing, name="show_pairing")
]