from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing,Comment, Bid


def index(request):
    activelisting = Listing.objects.filter(is_active = True)
    all_categories = Category.objects.all()

    return render(request, "auctions/index.html",{
            "listings":activelisting,
            "categories":all_categories
    })
def display_category(request):
    if request.method == "POST":
        categoryform = request.POST['category']
        category = Category.objects.get(category_name=categoryform)
        all_categories = Category.objects.all()   
        listings = Listing.objects.filter(category=category)
        return render(request, "auctions/index.html",{
            "listings":listings,
            "categories":all_categories
        })
    else:
        return HttpResponseRedirect(reverse("index"))
    
def listing(request,id):
    # Check if the listing exists
    is_in_watchlist = request.user in Listing.objects.get(pk=id).watchlist.all()
    listing = Listing.objects.get(pk=id)
    all_categories = Category.objects.all()
    all_comments = Comment.objects.filter(listing=listing)
    is_owner = request.user == listing.owner
    return render(request, "auctions/listing.html",{
        "listing": listing,
        "categories": all_categories,
        "is_in_watchlist": is_in_watchlist,
        "comments": all_comments,
        "is_owner": is_owner
    })

def add_to_watchlist(request, id):
    if request.method == "POST":
        # get the listing by id
        listing = Listing.objects.get(pk=id)
        # get the current user
        user = request.user
        # check if the user is authenticated
        if user.is_authenticated:
            # add the user to the watchlist of the listing
            listing.watchlist.add(user)
            return HttpResponseRedirect(reverse("listing", args=(id,)))
        else:
            return render(request, "auctions/login.html", {
                "message": "You must be logged in to add to watchlist."
            })
    else:
        return HttpResponseRedirect(reverse("index"))
def remove_from_watchlist(request, id):
    if request.method == "POST":
        # get the listing by id
        listing = Listing.objects.get(pk=id)
        # get the current user
        user = request.user
        # check if the user is authenticated
        if user.is_authenticated:
            # remove the user from the watchlist of the listing
            listing.watchlist.remove(user)
            return HttpResponseRedirect(reverse("listing", args=(id,)))
        else:
            return render(request, "auctions/login.html", {
                "message": "You must be logged in to remove from watchlist."
            })
    else:
        return HttpResponseRedirect(reverse("index"))
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

def create_listing(request):
    if request.method =="GET":
        all_categories = Category.objects.all()
        return render(request, "auctions/create_listing.html",{
            "categories": all_categories
        })
    else:
        title = request.POST['title']
        description = request.POST['description']
        image_url = request.POST['image_url']
        price = request.POST['Price']
        category = request.POST['category']
        # User info
        Current_user = request.user

        #create a new bid
        bid = Bid(
            bidder=Current_user,
            amount=price
        )
        # save the new bid
        bid.save()
        # create new Listing
        new_Listing = Listing(
            title=title,
            description=description,
            image_url=image_url,
            price= bid,
            category=Category.objects.get(category_name=category),
            owner=Current_user
        )
        # save the new listing
        new_Listing.save()
        return HttpResponseRedirect(reverse("index"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# place a bid on a listing
def place_bid(request, id):
    if request.method == "POST":
        # get the listing by id
        listing = Listing.objects.get(pk=id)
        # get the current user
        user = request.user
        # check if the user is authenticated
        if user.is_authenticated:
            # get the bid amount from the form
            bid_amount = request.POST['bid_amount']
            # create a new bid
            new_bid = Bid(
                bidder=user,
                amount=bid_amount
            )
            # save the new bid
            new_bid.save()
            # update the listing price with the new bid
            if listing.price is None or  float(new_bid.amount) > float(listing.price.amount):
                listing.price = new_bid
                listing.save()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "message": "Your bid has been placed successfully!"
                })
            
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "message": "Your bid must be higher than the current price."
                })
    else:
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

# display the watchlist
def watchlist(request):
    if request.user.is_authenticated:
        watchlist_items = request.user.watchlist.all()
        return render(request,"auctions/watchlist.html",{
            "watchlist_items": watchlist_items
        })
def add_comment(request, id):
    if request.method == "POST":
        content = request.POST['comment']
        listing = Listing.objects.get(pk=id)
        writer = request.user

        new_comment = Comment(
            listing=listing,
            writer=writer,
            content=content
        )
        new_comment.save()

        # Build URL with query parameter
        url = f"{reverse('listing', args=(id,))}?message=Comment+added+successfully!"
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(reverse("index"))
    
def close_listing(request, id):
        listing = Listing.objects.get(pk=id)
        listing.is_active = False
        listing.save()
        return render(request, "auctions/listing.html",{
        "listing": listing,
        "message": "Listing has been closed successfully!"
        
    })
