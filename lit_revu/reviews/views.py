from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Ticket, Review, UserFollows
from .forms import TicketForm, ReviewForm, UserFollowsForm
from django.contrib.auth.decorators import login_required


# Tickets


# Create
@login_required
def ticket_create(request):
    form = TicketForm()
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            return redirect("home")

    return render(request, "reviews/ticket_form.html", locals())


@login_required
def ticket_and_review_create(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect("home")

    return render(request, "reviews/ticket_and_review_form.html", locals())


# Read
@login_required
def ticket_list(request):
    followed_by_user = UserFollows.objects.filter(user=request.user).values_list(
        "followed_user", flat=True
    )
    tickets = Ticket.objects.filter(
        user__in=list(followed_by_user) + [request.user.id]
    ).order_by("-time_created")

    return render(request, "reviews/ticket_list.html", {"tickets": tickets})


@login_required
def ticket_content(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    followed_by_user = UserFollows.objects.filter(user=request.user).values_list(
        "followed_user", flat=True
    )
    if ticket.user.id not in followed_by_user and ticket.user != request.user:
        return redirect("home")

    return render(request, "reviews/ticket.html", {"ticket": ticket})


@login_required
def user_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
    return render(request, "reviews/ticket_list.html", {"tickets": tickets})


# Update
@login_required
def ticket_update(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    if request.method == "POST":
        if request.FILES.get("image") and ticket.image:
            ticket.image.delete(save=False)

        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("ticket", ticket.id)
    else:
        form = TicketForm(instance=ticket)

    return render(request, "reviews/ticket_form.html", locals())


# Delete
@login_required
def ticket_delete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    if request.method == "POST":
        if ticket.image:
            ticket.image.delete(save=False)
        ticket.delete()
        return redirect("home")
    return render(request, "reviews/delete.html", {"ticket": ticket})


# User reviews


# Create
@login_required
def review_create(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect("ticket", ticket.id)

    return render(request, "reviews/review_form.html", locals())


# Read
@login_required
def review_list(request):
    review = Review.objects.all()
    return render(request, "reviews/ticket_list.html", {"review": review})


# Update
@login_required
def review_update(request, review_id):
    review = Review.objects.get(id=review_id, user=request.user)
    ticket = review.ticket
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("ticket", review.ticket.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/review_form.html", locals())


# Delete
@login_required
def review_delete(request, review_id):
    review = Review.objects.get(id=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        return redirect("home")

    return render(request, "reviews/delete.html", {"review": review})


# User followers


# Read / Create
@login_required
def user_followers(request):
    # Récupérer les abonnés et les utilisateurs suivis
    followers = UserFollows.objects.filter(followed_user=request.user)
    following = UserFollows.objects.filter(user=request.user)

    if request.method == "POST":
        # Formulaire pour ajouter un abonnement
        form = UserFollowsForm(request.POST, user=request.user)
        if form.is_valid():
            followed_user = form.cleaned_data["followed_user"]

            if UserFollows.objects.filter(
                user=request.user, followed_user=followed_user
            ).exists():
                messages.error(request, "Vous suivez déjà cet utilisateur.")
            elif followed_user == request.user:
                messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
            else:
                UserFollows.objects.create(
                    user=request.user, followed_user=followed_user
                )
            return redirect("user_followers")
    else:
        form = UserFollowsForm(user=request.user)

    return render(request, "reviews/user_followers.html", locals())


# Delete
@login_required
def user_followers_delete(request, follow_id):
    user = UserFollows.objects.get(id=follow_id, user=request.user)
    if request.method == "POST":
        user.delete()
        return redirect("user_followers")
    return render(request, "reviews/user_followers.html", {"user": user})


# Ask user to create a Post or a Thread
@login_required
def post_or_thread(request):
    return render(request, "reviews/post_or_thread.html")
