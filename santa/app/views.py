from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse

from .models import Draw, Participant, Pairing

from random import choice, shuffle

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
        "is_drawn": draw.is_drawn,
    }

    return render(request, "draw_details.html", context)

def draw_edit(request, draw_id):
    draw = get_object_or_404(Draw, pk=draw_id)
    context = {
        "draw_name": draw.draw_name,
        "draw_pk": draw_id,
        "participants": draw.participants.all(),
    }
    if request.method == "POST":
        draw_name = request.POST.get("draw-name")
        names = request.POST.getlist("names")

        if draw.is_drawn:
            return HttpResponse("HTTP 403 - Forbidden, already drawn", status=403)

        if draw_name:
            draw.draw_name = draw_name
            draw.save()
        if names:
            draw.participants.all().delete()
            for name in names:
                if name:
                    participant = Participant(name=name, in_draw=draw)
                    participant.save()
        else:
            context["errors"] = "The draw cannot be empty"
            return render(request, "draw_edit.html", context)

        return redirect("draw_details", draw_id = draw.id)

    return render(request, "draw_edit.html", context)

def share_link(request, draw_id):
    draw = get_object_or_404(Draw, pk=draw_id)

    context = {
        "draw_name": draw.draw_name,
        "draw_pk": draw_id,
    }

    return render(request, "share_link.html", context)

def do_draw(request, draw_id):
    draw = get_object_or_404(Draw, pk=draw_id)

    context = {
        "draw_name": draw.draw_name,
        "draw_pk": draw_id,
        "participants": draw.participants.all(),
    }

    return render(request, "do_draw.html", context)

def participant_draw(request, draw_id, participant_id):
    draw = get_object_or_404(Draw, pk=draw_id)
    participant = get_object_or_404(Participant, pk=participant_id)

    if participant.in_draw.id != draw.id:
        return HttpResponse("HTTP 400 - Bad Request", status=400)
    
    if not draw.is_drawn:
        _do_draw(draw)

    participant = get_object_or_404(Participant, pk=participant_id)
    pairing = participant.to_gift
    
    return redirect("show_pairing", draw_id = draw.id, pairing_id = pairing.id)

def _do_draw(draw):
        draw.is_drawn = True
        draw.save()

        all_participants = list(Participant.objects.filter(in_draw=draw))
        shuffle(all_participants)

        recievers = _rotate_list(all_participants, 1)

        for i in range(len(all_participants)):
            pairing = Pairing(gifter=all_participants[i], giftee=recievers[i], draw=draw)
            pairing.save()
            all_participants[i].to_gift = pairing
            all_participants[i].save()

        return

def _rotate_list(l, n):
    return l[-n:] + l[:-n]

def show_pairing(request, draw_id, pairing_id):
    draw = get_object_or_404(Draw, pk=draw_id)
    pairing = get_object_or_404(Pairing, pk=pairing_id)

    context = {
        "draw_name": draw.draw_name,
        "gifter_name": pairing.gifter.name,
        "giftee_name": pairing.giftee.name,
        "details_link": f"/draw/{draw.id}",
    }

    return render(request, "pairing_result.html", context)