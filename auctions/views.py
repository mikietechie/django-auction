from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User,Listing,Category,Watch,Comment


def index(request):
    context = {}
    context['title'] = "All Listings"
    context['listings'] = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html",context)

@login_required(login_url='login')
def comment(request):
    if request.POST:
        #user=User.objects.get(username=request.POST['user'])
        #listing = Listing.objects.get(pk=request.POST['listing'])
        #msg = request.POST['msg']
        comment = Comment(msg=request.POST['msg'],listing=Listing.objects.get(pk=request.POST['listing']),user=User.objects.get(username=request.POST['user']))
        comment.save()
        return view(request,Listing.objects.get(pk=request.POST['listing']).id)

@login_required(login_url='login')
def view(request,id):
    context = {}
    listing = Listing.objects.get(pk=id)
    context['listing'] = listing
    context['comments'] = Comment.objects.filter(listing=listing)
    if request.POST:
        #user=User.objects.get(username=request.POST['user'])
        try:
            listing.active = eval(request.POST['close_listing'])
            listing.save()
            return index(request)
        except:
            pass

        #else:
        phase1 = ''
        phase2 = ''
        try:
            posted_minBid = eval(request.POST['minBid'])
            if posted_minBid > listing.minBid:
                listing.bids = listing.bids+1
                listing.minBid = posted_minBid
                listing.highestBidder = User.objects.get(username=request.POST['user'])
                listing.save()
                print('successfully bidded')
                phase1 = 'pos' # declare bidding as successful
            else:
                print('is less')
                phase1 = 'neg'
        except:
            print('something went wrong in bidding')
            phase1 = ''
        try:
            if request.POST['addwatch'] == 'on':
                if Watch.objects.filter(user=User.objects.get(username=request.POST['user']), listing=listing):
                    phase2 = 'neg'
                    print('watch exists')
                else:
                    prospective_watch = Watch(user = User.objects.get(username=request.POST['user']), listing=listing)
                    prospective_watch.save()
                    phase2 = 'pos'
                    print('created watch')
            else:
                print('watch was off')
        except:
            phase2 = ''
            print('failed addwatch test')
        if ((phase1 == '') and (phase2 == '')):
            context['msg'] = 'No data posted'
            return render(request,'auctions/view.html',context)
        elif ((phase1 == 'neg') and (phase2 == 'neg')):
            context['msg'] = 'Errors in posted data!!!, bid should be greater than current bid and or tick add watch input'
            return render(request,'auctions/view.html',context)
        elif ((phase1 == 'pos') and (phase2 == 'pos')):
            context['msg'] = 'Operations successful'
            return render(request,'auctions/view.html',context)
        elif ((phase1 == 'neg') and (phase2 == 'pos')):
            context['msg'] = f'Successfully added to watch list, however your bid should be greater than {listing.minBid}.'
            return render(request,'auctions/view.html',context)
        elif ((phase1 == 'pos') and (phase2 == 'neg')):
            context['msg'] = 'Successfully bidded and you already have this listing on your watchlist.'
            return render(request,'auctions/view.html',context)
        elif ((phase1 == 'pos') and (phase2 == '')):
            context['msg'] = 'Successfully bidded'
            return render(request,'auctions/view.html',context)
        elif ((phase1 == '') and (phase2 == 'pos')):
            context['msg'] = 'Successfully added to watch list'
            return render(request,'auctions/view.html',context)
        elif ((phase1 == 'neg') and (phase2 == '')):
            context['msg'] = f'Bid failed please make sure your bid is greater than {listing.minBid}'
            return render(request,'auctions/view.html',context)
        elif ((phase1 == '') and (phase2 == 'neg')):
            context['msg'] = 'Its already on your watchlist'
            return render(request,'auctions/view.html',context)

    return render(request,'auctions/view.html',context)



@login_required(login_url='login')
def removewatchitem(request,user,id):
    context = {}
    listing = Listing.objects.get(pk=id)
    user = User.objects.get(username=user)
    try:
        watchitem = Watch.objects.get(user=user,listing=listing)
        watchitem.delete()
        context['result'] = 'successfully removed thelisting from your watchlist'
    except:
        context['result'] ='failed to remove item from your watchlist'
    context['listings'] = Watch.objects.filter(user=User.objects.get(username=user))
    return render(request,'auctions/watchlist.html',context)

@login_required(login_url='login')
def watchlist(request,user):
    context = {}
    context['listings'] = Watch.objects.filter(user=User.objects.get(username=user))
    return render(request,'auctions/watchlist.html',context)

@login_required(login_url='login')
def category(request,name):
    context = {}
    if name == 'all':
        context['categories'] = Category.objects.all()
        return render(request,'auctions/category.html',context)
    categoryID = Category.objects.get(name=name)
    context['title'] = f'Category : {name}'
    context['listings'] = Listing.objects.filter(category=categoryID,active=True)
    return render(request,'auctions/index.html',context)

@login_required(login_url='login')
def new(request):
    context = {}
    context['categories'] = Category.objects.all()
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        minBid = request.POST['minBid']
        imgURL = request.POST['imgURL']
        category = Category.objects.get(pk=int(request.POST['category']))
        seller = User.objects.get(username=request.POST['user'])
        prospective_listing = Listing(title=title,description=description,minBid=minBid,imgURL=imgURL,category=category,seller=seller)
        try:
            prospective_listing.save()
            context['msg'] = f'Successfully posted {title} !!!'
            return render(request, "auctions/new.html",context)
        except:
            context['msg'] = f'Error in the {title} you posted please provide title,description and minimum bid !!!'
            return render(request, "auctions/new.html",context)
    return render(request, "auctions/new.html",context)


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
