from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def listing(request, listing_id):
    # Access the Listing from db
    listing = Listing.objects.get(pk=listing_id)

    # Ensure Listing in watchlist
    is_listing_in_watchlist = request.user in listing.watchlist.all()

    # Filter comments associated with Listing
    comments = Comment.objects.filter(listing=listing).order_by('-date_posted')

    # Ensure only listing owner can comment and add listing to watchlist
    is_owner = request.user.username == listing.owner.username

    # Display Listing and associated comments
    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'is_listing_in_watchlist': is_listing_in_watchlist,
        'comments': comments,
        'is_owner': is_owner
    })  

def closedlistings_view(request):
    # Filter closed listings in db
    closed_listings = Listing.objects.filter(is_active=False)

    # Display closed listings
    return render(request, "auctions/closedlistings.html",{
        'closed_listings': closed_listings,
    })

def closelisting(request, listing_id):
    # Access the Listing from db
    listing = Listing.objects.get(pk=listing_id)
    # Set Listing's status to inactive and save
    listing.is_active = False
    listing.save()

    # Ensure Listing in watchlist
    is_listing_in_watchlist = request.user in listing.watchlist.all()

    # Ensure only listing owner can close the Listing
    is_owner = request.user.username == listing.owner.username

    # Filter comments associated with Listings, order by date posted
    comments = Comment.objects.filter(listing=listing).order_by('-date_posted')

    # Update Listing to Closed + display Congrats message
    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'is_listing_in_watchlist': is_listing_in_watchlist,
        'comments': comments,
        'is_owner': is_owner,
        'update': True,
        'message': 'Congratulations! Your auction has ended. Please look for and bid on other listings.'
    })
    

def addbid(request, listing_id):
    # Get new bid from submitted form data
    new_bid = float(request.POST['bid'])

    # Access the Listing from db
    listing = Listing.objects.get(pk=listing_id)

    # Ensure Listing in Watchlist
    is_listing_in_watchlist = request.user in listing.watchlist.all()

    # Filter comments associated with Listings, order by date posted
    comments = Comment.objects.filter(listing=listing).order_by('-date_posted')

    # Ensure only listing owner can close the Listing
    is_owner = request.user.username == listing.owner.username

    # Esnure new bid > Listing's current bid, dislay successful message
    if new_bid > listing.price.bid:
        # Add new bid to db
        bid = Bid(author=request.user, bid=new_bid)
        bid.save()

        # Update Listing's price
        listing.price = bid
        listing.save()

        # Display updated Listing + success msg
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'is_listing_in_watchlist': is_listing_in_watchlist,
            'comments': comments,
            'message': 'Your bid has been received and the current bid has been updated successfully!',
            'update': True,
            'is_owner': is_owner,
        })
    else:
        # Display failure msg
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'is_listing_in_watchlist': is_listing_in_watchlist,
            'comments': comments,
            'message': 'Your bid must be greater than the current bid amount above',
            'update': False,
            'is_owner': is_owner,
        })


def addcomment(request, listing_id):
    # Access User currently logged in
    current_user = request.user

    # Access Listing from DB
    listing = Listing.objects.get(pk=listing_id)
    
    # Get user's comment from submitted form
    comment = request.POST['message']

    # Create new coment and save to db
    newmessage = Comment(
        author=current_user,
        listing=listing,
        message=comment
    )
    newmessage.save()

    # Redirect user to Listing page
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def watchlist(request):
    # Access User currently logged in
    current_user = request.user

    # Filter listings in watchlist of current user
    listings = current_user.listingwatchlist.all()

    # Dislayed watchlist listings
    return render(request, 'auctions/watchlist.html', {
        'listings': listings
    })
    pass

def addwatchlist(request, listing_id):
    # Access Listing from DB
    listing = Listing.objects.get(pk=listing_id)
    
    # Access User currently logged in
    current_user = request.user

    # Add Listing to watchlist of current user
    listing.watchlist.add(current_user)

    # Redirect user to the listing page
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def removewatchlist(request, listing_id):
    # Access Listing from DB
    listing = Listing.objects.get(pk=listing_id)

    # Access User currently logged in
    current_user = request.user

    # Remove listing from watchlist of current user
    listing.watchlist.remove(current_user)

    # Redirect user to Listing page
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def index(request):

    # Filter listings currently active
    active_listings = Listing.objects.filter(is_active=True).order_by('-date_created')

    # Access categories from db
    categories = Category.objects.all()

    # Diesplay active listings and categories
    return render(request, "auctions/index.html",{
        'active_listings': active_listings,
        'categories': categories,
    })


def category_view(request):
    if request.method == 'POST':
        # Access category from submitted data form
        category_form = request.POST['category']

        # Find category based on submitted data
        category = Category.objects.get(category_name=category_form)

        # Filter active listings associated with the category
        active_listings = Listing.objects.filter(is_active=True, category=category)

        # Access categories from db
        categories = Category.objects.all()

        # Dislpay active listings associated with the category
        return render(request, "auctions/index.html",{
            'active_listings': active_listings,
            'categories': categories,
        })


def create_listing(request):

    # For GET request when user click a link
    if request.method == 'GET':

        # Get all categories from database
        categories = Category.objects.all()

        # Dilay Create form with all categories
        return render(request, 'auctions/create.html', {
            'categories': categories
        })

    # For a post request, create a new Listing
    else:
        # Access submitted form data
        title = request.POST['title']
        description = request.POST['description']
        img_url = request.POST['img_url']
        price = float(request.POST['price'])
        category = request.POST['category']
        owner = request.user
        
        # Create an Category obj
        cat_obj = Category.objects.get(category_name=category)

        # Create a Bid obj
        bid = Bid(bid=price, author=owner)
        bid.save()

        # Create a Listing obj
        listing = Listing(
            title=title,
            description=description,
            img_url=img_url,
            price=bid,
            owner=owner,
            category=cat_obj
        )
        listing.save()

        # Redirect user to index page
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
