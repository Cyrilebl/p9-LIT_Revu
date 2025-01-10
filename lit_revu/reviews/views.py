from django.shortcuts import render
from .models import Ticket
from django.contrib.auth.decorators import login_required


@login_required
def ticket_list(request):
    ticket = Ticket.objects.all()
    return render(request, "reviews/ticket_list.html", {"tickets": ticket})


@login_required
def ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, "reviews/ticket_detail.html", {"ticket": ticket})
