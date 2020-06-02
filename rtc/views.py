from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
from rtc.models import Room


@login_required
def index(request):
    rooms = Room.objects.order_by("title")

    return render(request, "index.html", {
        "rooms": rooms,
    })
