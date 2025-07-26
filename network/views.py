from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import User, Post



# Returns the home page with all posts.
def index(request):
    allPosts = Post.objects.all().order_by('-dateCreated')
    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}

    return render(request, 'network/index.html', context)



# Creates a user Post in Database
@login_required
def submitPost(request):
    if request.method == 'POST':
        content = request.POST.get('postContent')
        user = request.user

        # create a new post object
        Post.objects.create(user=user, postContent=content)

        return HttpResponseRedirect(reverse("index"))

    return HttpResponse("Only POST requests are accepted.")





@login_required
def profileView(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=profile_user).order_by('-dateCreated')
    is_following = request.user in profile_user.followers.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/profile.html', {
        "profile_user": profile_user,
        'page_obj': page_obj,
        "is_following": is_following
    })





@login_required
def follow_user(request, user_id):
    if request.method == "POST":
        target = get_object_or_404(User, id=user_id)
        if request.user != target:
            request.user.following.add(target)
    return redirect('profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    if request.method == "POST":
        target = get_object_or_404(User, id=user_id)
        if request.user != target:
            request.user.following.remove(target)
    return redirect('profile', user_id=user_id)

@login_required
def followingPage(request):
    followed_users = request.user.following.all()
    posts = Post.objects.filter(user__in=followed_users).order_by('-dateCreated')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}


    return render(request, 'network/following.html', context)


@login_required
@csrf_exempt  # optional if you're using fetch with csrf token
def edit_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "").strip()

        try:
            post = Post.objects.get(pk=post_id, user=request.user)
            post.postContent = content
            post.save()
            return JsonResponse({"success": True})
        except Post.DoesNotExist:
            return JsonResponse({"success": False, "error": "Post not found or not yours"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required
def like_toggle(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get('post_id')

        post = get_object_or_404(Post, id=post_id)

        liked = False
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            "liked": liked,
            "total_likes": post.likes.count()
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)



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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
