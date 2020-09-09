from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, UserFriend
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
import datetime


# Get all posts - API 
def load_posts(request):
    post_list = Post.objects.all()
    posts = post_list.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)




# Add friend - API
@csrf_exempt
@login_required
def accept_friend(request):
     # Must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get data
    data = json.loads(request.body)
    profile_username = data.get("body", "")

    current_user = User.objects.get(username=request.user)
    profile_user = User.objects.get(username=profile_username)


    friend_request = UserFriend(
        user_id=profile_user,
        friending_user_id=current_user
    )
    friend_request.save()

    return JsonResponse({"message": "Friend accepted successfully."}, status=201)



# Add friend - API
@csrf_exempt
@login_required
def add_friend(request):
     # Must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Must log in 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('weather:login'))

    # Get data
    data = json.loads(request.body)
    profile_username = data.get("body", "")

    current_user = User.objects.get(username=request.user)
    profile_user = User.objects.get(username=profile_username)


    friend_request = UserFriend(
        user_id=profile_user,
        friending_user_id=current_user
    )
    friend_request.save()

    return JsonResponse({"message": "Friend requested successfully."}, status=201)



# Create your views here.
def homepage(request):
    post_list = Post.objects.all()
    post_list = post_list.order_by("-timestamp").all()

    current_user = request.user.username
    # Get current time 
    now = datetime.datetime.now()

    return render(request, "weather/homepage.html", {
        'posts': post_list,
        'current_user': current_user,
        'now': now,
    })


@csrf_exempt
def friend_request(request):
    # Must log in 
    if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('weather:login'))
    
    # Get every obj where the current user has been added by others, for friend requests 
    friend_relations = UserFriend.objects.filter(user_id__username=request.user)
    # All obj current user sent friend requests to
    user_added = UserFriend.objects.filter(friending_user_id__username=request.user.username)

    
    requested_from = []
    for friend in friend_relations:
        requested_from.append(friend.friending_user_id)

    request_to = []
    for i in user_added:
        request_to.append(i.user_id)
    
    requested_from_only = set(requested_from) - set(request_to)

    
    

    return render(request, "weather/friend_request.html", {
        "friend_relations": friend_relations,
        "user_added": user_added,
        "requested_from": requested_from,
        "request_to": request_to,
        "requested_from_only":requested_from_only,
    })


@csrf_exempt
def friend_list(request):
    # Must log in 
    if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('weather:login'))

    # Get every obj where the current user has been added, for friend requests 
    friend_relations = User.objects.filter(being_friended__friending_user_id__username=request.user)
    ##### Test ##### friends = UserFriend.objects.filter(user_id__username__in=[i.friending_user_id for i in friend_relations]).distinct()
    
    # friending _ _ user_id TWO UNDFERSCORE
    friends = User.objects.filter(friending__user_id__username=request.user)


    return render(request, "weather/friend_list.html", {
        "friend_relations": friend_relations,
        "friends": friends,

    })

# Structure of the profile page
@csrf_exempt
def profile_page(request, username):
    # Get current user 
    try: 
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        user = None
    # Get profile user 
    try:
        profile = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Profile not found.")
    # Find out if user have sent friend request already
    try:
        friend_relations = UserFriend.objects.get(user_id__username=username, friending_user_id__username=user)
    except UserFriend.DoesNotExist:
        friend_relations = None
    # For profile user most recent post 
    post_list = Post.objects.filter(poster__username=username)

    return render(request, "weather/profile.html", {
        "post_list": post_list,
        "profile": profile,
        "friend_relations": friend_relations,
    })


# Api for fetching data
@csrf_exempt
@login_required
def compose(request): 
     # Composing a new posts must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get contents of post
    data = json.loads(request.body)
     
    content = data.get("body", "")

    post = Post(
        poster=request.user,
        content=content
    )
    post.save()

    return JsonResponse({"message": "Post created successfully."}, status=201)



    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("weather:homepage"))
        else:
            return render(request, "weather/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "weather/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("weather:homepage"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "weather/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "weather/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("weather:homepage"))
    else:
        return render(request, "weather/register.html")
