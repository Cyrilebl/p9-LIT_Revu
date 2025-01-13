from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket
from .forms import TicketForm
from django.contrib.auth.decorators import login_required
from authentication.models import User


# Create
@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("ticket_list")
    else:
        form = TicketForm()

    return render(request, "reviews/ticket_create.html", {"form": form})


# Read
@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, "reviews/ticket_list.html", {"tickets": tickets})


@login_required
def ticket_content(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, "reviews/ticket_content.html", {"ticket": ticket})


# Update
@login_required
def ticket_update(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("ticket_content", ticket.id)
    else:
        form = TicketForm(instance=ticket)

    return render(request, "reviews/ticket_update.html", {"form": form})


# Delete
@login_required
def ticket_delete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        return redirect("ticket_list")
    return render(request, "reviews/ticket_delete.html", {"ticket": ticket})


# User posts
@login_required
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    tickets = Ticket.objects.filter(user=user).order_by("-time_created")

    context = {
        "user_profile": user,
        "tickets": tickets,
    }
    return render(request, "reviews/user_posts.html", context)
