from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, UserFollowsForm
from django.contrib.auth.decorators import login_required
from authentication.models import User


# Tickets


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
    return render(request, "reviews/ticket.html", {"ticket": ticket})


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

    return render(request, "reviews/ticket_form.html", {"form": form, "ticket": ticket})


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
    return render(request, "reviews/ticket_list.html", context)


# User comments


# Create
@login_required
def review_create(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("ticket_content", ticket.id)
    else:
        form = ReviewForm()

    return render(request, "reviews/review_form.html", {"form": form, "ticket": ticket})


# Read
@login_required
def review_list(request):
    reviews = Review.objects.all()
    return render(request, "reviews/ticket_list.html", {"reviews": reviews})


# Update
@login_required
def review_update(request, ticket_id, review_id):
    review = Review.objects.get(id=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("ticket_content", ticket_id)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/review_form.html", {"form": form})


# Delete
@login_required
def ticket_delete(request, review_id):
    review = Review.objects.get(id=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        return redirect("ticket_list")
    return render(request, "reviews/ticket_delete.html", {"review": review})


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
