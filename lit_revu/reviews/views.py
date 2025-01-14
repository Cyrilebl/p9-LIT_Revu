from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, UserFollows
from .forms import TicketForm, UserFollowsForm
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

    return render(request, "reviews/ticket_form.html", {"form": form})


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

    return render(request, "reviews/ticket_form.html", {"form": form})


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


# User followers


# Read / Create
@login_required
def user_followers(request, username):
    target_user = get_object_or_404(User, username=username)

    # Récupérer les abonnés et les utilisateurs suivis
    followers = UserFollows.objects.filter(followed_user=target_user)
    following = UserFollows.objects.filter(user=target_user)

    if request.method == "POST":
        # Formulaire pour ajouter un abonnement
        form = UserFollowsForm(request.POST, user=request.user)
        if form.is_valid():
            followed_user = form.cleaned_data["followed_user"]
            if UserFollows.objects.filter(
                user=request.user, followed_user=followed_user
            ).exists():
                messages.error(request, "Vous suivez déjà cet utilisateur.")
            else:
                follow = form.save(commit=False)
                follow.user = request.user
                follow.save()
            return redirect("user_followers", username=username)
    else:
        form = UserFollowsForm(user=request.user)

    context = {
        "form": form,
        "target_user": target_user,
        "followers": followers,
        "following": following,
    }
    return render(request, "reviews/user_followers.html", context)


# Delete
@login_required
def user_followers_delete(request, username, follow_id):
    user = get_object_or_404(UserFollows, id=follow_id, user=request.user)
    if request.method == "POST":
        user.delete()
        return redirect("user_followers", username=username)
    return render(request, "reviews/user_followers.html", {"user": user})
