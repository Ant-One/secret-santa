from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.template.defaultfilters import slugify
from django.http import HttpResponse

from .models import Draw, Participant, Pairing

from random import choice, shuffle, sample

from django.db.models import Count

# Create your views here.

def index(request):
    return render(request, "index.html")

def new_draw(request):
    return render(request, "new_draw.html")

def create_draw(request):
    if request.method == "POST":
        draw_name = request.POST.get("draw-name")
        names = request.POST.getlist("names")

        error = "None"

        if not draw_name or not names:
            return HttpResponse("HTTP 400 - Bad Request", status=400)
        
        draw = Draw(draw_name=draw_name)
        draw.save()
        for name in names:
            if name:
                participant = Participant(name=name, name_slug=slugify(name), in_draw=draw)
                participant.save()

        if len(set(names)) != len(names):
            error = "Two or more names are identical!"

            context = {
                "draw_name": draw.draw_name,
                "draw_pk": draw.id,
                "participants": draw.participants.order_by("name"),
                "errors": error
            }

            return render(request, "draw_edit", context)

    return redirect("draw_details", draw_id = draw.id)

def draw_details(request, draw_id):
    draw = get_object_or_404(Draw, pk=draw_id)

    if draw.is_drawn:
        return redirect("do_draw", draw_id = draw.id)

    context = {
        "draw_name": draw.draw_name,
        "participants": draw.participants.order_by("name"),
        "is_drawn": draw.is_drawn,
    }

    return render(request, "draw_details.html", context)

def draw_edit(request, draw_id):
    draw = get_object_or_404(Draw, pk=draw_id)
    context = {
        "draw_name": draw.draw_name,
        "draw_pk": draw_id,
        "participants": draw.participants.order_by("name"),
    }
    if request.method == "POST":
        draw_name = request.POST.get("draw-name")
        names = request.POST.getlist("names")

        error = None

        if draw.is_drawn:
            return HttpResponse("HTTP 403 - Forbidden, already drawn", status=403)

        if draw_name:
            draw.draw_name = draw_name
            draw.save()
        if names:
            print(f"set {len(set(names))}, lennames {len(names)}")

            draw.participants.all().delete()
            for name in names:
                if name:
                    participant = Participant(name=name, in_draw=draw)
                    participant.save()

                    if len(set(names)) != len(names):
                        error = "Two or more names are identical!"
        else:
            context["errors"] = "The draw cannot be empty"
            return render(request, "draw_edit.html", context)
        
        if error:
            context = {
                            "draw_name": draw.draw_name,
                            "draw_pk": draw_id,
                            "participants": draw.participants.order_by("name"),
                            "errors": error
                        }
            return render(request, "draw_edit.html", context)

        return redirect("draw_details", draw_id = draw.id)

    return render(request, "draw_edit.html", context)

def draw_exclusions(request, draw_id):
    draw = get_object_or_404(Draw, pk=draw_id)
    context = {
        "draw_name": draw.draw_name,
        "draw_pk": draw_id,
        "participants": draw.participants.order_by("name"),
    }

    if request.method == "POST":
        all_participants = list(Participant.objects.filter(in_draw=draw))

        for participant in all_participants:
            participant_exclusions = request.POST.getlist(f"exclusions-{participant.name_slug}")
            participant.exclusions.clear()
            for exclusion in participant_exclusions:
                if exclusion:
                    print(exclusion)
                    exclusion_person = Participant.objects.get(name = exclusion, in_draw=draw)
                    participant.exclusions.add(exclusion_person)
            participant.save()

        return redirect("draw_details", draw_id = draw.id)

    return render(request, "draw_exclusions.html", context)

def share_link(request, draw_id):
    draw = get_object_or_404(Draw, pk=draw_id)

    context = {
        "draw_name": draw.draw_name,
        "draw_pk": draw_id,
    }

    return render(request, "share_link.html", context)

def do_draw(request, draw_id):
    draw = get_object_or_404(Draw, pk=draw_id)

    if not draw.is_drawn:
        e = _do_draw(draw)
        if e:
            return e

    context = {
        "draw_name": draw.draw_name,
        "draw_pk": draw_id,
        "participants": draw.participants.order_by("name"),
    }

    return render(request, "do_draw.html", context)

def participant_draw(request, draw_id, participant_id):
    draw = get_object_or_404(Draw, pk=draw_id)
    participant = get_object_or_404(Participant, pk=participant_id)

    if participant.in_draw.id != draw.id:
        return HttpResponse("HTTP 400 - Bad Request", status=400)

    participant = get_object_or_404(Participant, pk=participant_id)
    pairing = participant.to_gift
    
    return redirect("show_pairing", draw_id = draw.id, pairing_id = pairing.id)

def _do_draw(draw):
        MAX_TRIES = 100

        all_participants = Participant.objects.filter(in_draw=draw).annotate(exclusion_count=Count('exclusions')).order_by('-exclusion_count')

        possibility_dict = {}

        tentative_pairings = []

        for participant in all_participants:
            exclusions_id = participant.exclusions.values_list("pk", flat=True)
            possible_giftees = Participant.objects.filter(in_draw=draw).exclude(id__in=exclusions_id).exclude(id=participant.id)
            possibility_dict[participant.id] = list(possible_giftees.values_list("pk", flat=True))

        success = True

        for i in range(0, MAX_TRIES):
            try:
                tentative_pairings, parts_to_save = _try_pairing(all_participants, possibility_dict, draw)
                success = True
                break
            except Exception as e:
                print(e)
                success = False

        if not success:
            return HttpResponse("Matching failed", status=500)

        Pairing.objects.bulk_create(tentative_pairings)

        Participant.objects.bulk_update(parts_to_save, fields=["to_gift"])

        draw.is_drawn = True
        draw.save()

        return

def _try_pairing(all_participants, possibility_dict, draw):

    drawn = []
    pairings = []
    parts_to_save = []

    for participant in all_participants:
        for val in possibility_dict[participant.pk]:
            if val in drawn:
                possibility_dict[participant.pk].remove(val)

        matching = sample(possibility_dict[participant.pk], 1)
        if not matching[0]:
            raise Exception("Iteration failed")
        drawn.append(matching[0])
        p = Pairing(draw=draw, gifter=participant, giftee=Participant.objects.get(pk=matching[0]))
        participant.to_gift = p
        parts_to_save.append(participant)

        pairings.append(p)

    return pairings, parts_to_save

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