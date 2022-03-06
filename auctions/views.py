from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


def index(request):
    if "category" in request.GET and request.GET["category"] != "all":
        listings = Listing.objects.filter(closed=False, category=request.GET["category"])
    else:
        listings = Listing.objects.filter(closed=False)
    return render(request, "auctions/index.html", {
        'listings': listings,
        'categories': CATEGORY_CHOICES
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if "next" in request.POST:
                return HttpResponseRedirect(request.POST["next"])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    if "next" in request.GET:
        return HttpResponseRedirect(request.GET["next"])
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


# TODO: Create a new view specific to closed listings
def view_listing(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)

    if request.method == "POST":
        form = PlaceBidForm(request.POST, listing=current_listing)
        if form.is_valid():
            # Remove any previous bids made by the current user on this listing
            Bid.objects.filter(bidder=request.user, listing=current_listing).delete()

            bid_value = form.cleaned_data["value"]
            new_bid = Bid(bidder=request.user, listing=current_listing, value=bid_value)
            new_bid.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        form = PlaceBidForm(listing=current_listing)

    return render(request, "auctions/listing.html", {
        "listing": current_listing,
        "place_bid_form": form,
        "comments_list": current_listing.comments.all()
    })


@login_required
def add_comment(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        content = request.POST["content"]
        new_comment = Comment(commenter=request.user, content=content, listing=current_listing)
        new_comment.save()
        current_listing.comments.add(new_comment)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def delete_comment(request, comment_id):
    current_comment = Comment.objects.get(pk=comment_id)
    listing_id = current_comment.listing.id
    if current_comment.commenter == request.user:
        current_comment.delete()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.seller = request.user
            new_bid = Bid(bidder=request.user, listing=new_listing, value=form.cleaned_data["starting_bid"])
            
            new_listing.save()
            form.save_m2m()
            new_bid.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
    
    return render(request, "auctions/create_listing.html", {
        "form": form
    })


@login_required
def my_listings_view(request):
    return render(request, "auctions/index.html", {
        "listings": request.user.listings.all(),
    })


@login_required
def my_bids_view(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(bids__in=request.user.bids.all()),
    })


@login_required
def close_view(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    if request.user == current_listing.seller:
        current_listing.closed = True
        current_listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def modify_watchlist(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    if request.GET.get("how") == "add":
        current_listing.watchlisting_users.add(request.user)
    elif request.GET.get("how") == "remove":
        current_listing.watchlisting_users.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def watchlist_view(request):
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlist.all(),
    })
