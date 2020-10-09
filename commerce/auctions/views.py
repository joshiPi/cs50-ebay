from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import CreateListingForm
from .models import User, Listings, Comments, Bids


def index(request):

    listings = Listings.objects.all()
    return render(request, "auctions/index.html", {'listings': listings})


def active(request):

    listings = Listings.objects.filter(closed=False)
    return render(request, "auctions/index.html", {'listings': listings})


def search(request):
    q = request.GET['q']
    listings = Listings.objects.filter(category=q)
    if listings:
        return render(request, 'auctions/category_search.html', {'listings': listings, 'q': q})
    else:
        categories = list(set([e.category for e in Listings.objects.all()]))
        return render(request, 'auctions/category_search.html', {'categories': categories, 'q': q})


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
    try:
        bids = Bids.objects.get(bid_on=pk)
        value = bids.bid
    except:
        value = "No Current bids "

    listing = lg[0]
    comments = Comments.objects.filter(commented_on=pk)
    return render(request, 'auctions/listing.html', {'listing': listing, 'comments': comments, 'value': value})


@login_required
def bidding(request, pk):
    listing = Listings.objects.get(id=pk)
    if request.method == "POST":
        user_bid = request.POST['user_bid']
        user_bid = float(user_bid)
        try:
            bids = Bids.objects.get(bid_on=listing)
            current_bid = float(bids.bid)
            if user_bid > current_bid:
                bids.bid_by = request.user
                bids.bid = user_bid
                bids.save()
                message = "Your bid is successfully placed"

            else:
                message = "Your Current bid is lower than existing bid"
            return render(request, 'auctions/bidding.html', {"listing": listing, 'message': message})

        except:
            if user_bid > listing.starting_bid:
                user = request.user
                bid_instance = Bids(bid_by=user, bid_on=listing, bid=user_bid)
                bid_instance.save()
                message = "Your bid is successfully placed(e)"
            else:
                message = "Your Current bid is lower than existing bid(e)"
            return render(request, 'auctions/bidding.html', {"listing": listing, 'message': message})

    return render(request, 'auctions/bidding.html', {"listing": listing})

#     try:
#         bid = Bids.objects.get(bid_on=pk)


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


def close_listing(request, pk):
    lis = Listings.objects.get(id=pk)
    lis.closed = True
    lis.save()
    return HttpResponseRedirect(reverse('index'))


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
