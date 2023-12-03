from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse

from .models import Draw, Participant

# Create your views here.

def index(request):
    return render(request, "index.html")

def new_draw(request):
    return render(request, "new_draw.html")

def create_draw(request):
    if request.method == "POST":
        draw_name = request.POST.get("draw-name")
        names = request.POST.getlist("names")

        if not draw_name or not names:
            return HttpResponse("HTTP 400 - Bad Request", status=400)
        draw = Draw(draw_name=draw_name)
        draw.save()
        for name in names:
            if name:
                participant = Participant(name=name, in_draw=draw)
                participant.save()

    return redirect("draw_details", draw_id = draw.id)

def draw_details(request, draw_id):
    draw = get_object_or_404(Draw, pk=draw_id)

    context = {
        "draw_name": draw.draw_name,
        "participants": draw.participants.all(),
    }

    return render(request, "draw_details.html", context)

def draw_edit(request, draw_id):
    draw = get_object_or_404(Draw, pk=draw_id)
    if request.method == "POST":
        draw_name = request.POST.get("draw-name")
        names = request.POST.getlist("names")

        if draw_name:
            draw.draw_name = draw_name
        if names:
            draw.participants.all().delete()
            for name in names:
                participant = Participant(name=name, in_draw=draw)
                participant.save()

        return redirect("draw_details", draw_id = draw.id)

    context = {
        "draw_name": draw.draw_name,
        "draw_pk": draw_id,
        "participants": draw.participants.all(),
    }

    return render(request, "draw_edit.html", context)