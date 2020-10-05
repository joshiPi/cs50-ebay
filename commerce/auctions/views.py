from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.signals import user_logged_in
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateListingForm
from .models import User, Listings, Comments


def index(request):
    listings = Listings.objects.filter(closed=False)

    return render(request, "auctions/index.html", {'listings': listings})


def listing(request, pk):
    if request.method == "POST":
        comm = request.POST.get('comment')
        Listing = Listings.objects.get(id=pk)
        user = User.objects.get(id=request.user.id)
        new_comment = Comments(
            commented_by=user, commented_on=Listing, comment=comm)
        new_comment.save()
        return HttpResponseRedirect(reverse('listing', args=(pk,)))
    lg = Listings.objects.filter(id=pk)
    listing = lg[0]
    comments = Comments.objects.filter(commented_on=pk)
    return render(request, 'auctions/listing.html', {'listing': listing, 'comments': comments})


def watchlist(request, pk):

    wl = Listings.objects.filter(watchlist_user=pk)
    return render(request, 'auctions/watchlist.html', {'watchlist': wl})


def add_watchlist(request, pk):
    item = Listings.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)
    item.watchlist_user.add(user)
    return HttpResponseRedirect(reverse('watchlist', args=(request.user.id,)))


def remove_watchlist(request, pk):
    item = Listings.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)
    item.watchlist_user.remove(user)
    return HttpResponseRedirect(reverse('watchlist', args=(request.user.id,)))


def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            image_url = form.cleaned_data['image_url']
            category = form.cleaned_data['category']
            #closed = form.cleaned_data['closed']
            user = User.objects.get(id=request.user.id)
            new_listing = Listings(owner=user, title=title, description=description,
                                   starting_bid=starting_bid, category=category, image_url=image_url)
            new_listing.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = CreateListingForm()
        listings = Listings.objects.filter(owner=request.user.id)
    return render(request, 'auctions/create_listing.html', {'form': form, 'listings': listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
