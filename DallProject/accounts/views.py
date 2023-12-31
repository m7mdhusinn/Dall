
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import UserProfile
from posts.models import Post

# Create your views here.

def register_user_view(request: HttpRequest):
    msg = None

    if request.method == "POST":
        try:
            #create a new user
            user = User.objects.create_user(username=request.POST["username"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=request.POST["password"])
            user.save()

            user_profile = UserProfile(user=user)
            user_profile.save()

            return redirect("accounts:login_user_view")
        except IntegrityError as e:
            msg = f"Please select another username, {e}"
        except Exception as e:
            msg = f"something went wrong {e}"

    return render(request, "accounts/register.html", {"msg" : msg})


def login_user_view(request: HttpRequest):
    msg = None
    if request.method == "POST":
        #first : authenticate the user data
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user:
            #second: login the user
            login(request, user)
            return redirect("main:home_view")
        else:
            msg = "Please provide correct username and password"



    return render(request, "accounts/login.html", {"msg" : msg})



def logout_user_view(request: HttpRequest):

    #log out the user
    if request.user.is_authenticated:
        logout(request)    

    return redirect("accounts:login_user_view")



def user_profile_view(request: HttpRequest, user_id):
    msg=None
    try:

        user = UserProfile.objects.get(user=User.objects.get(id=user_id))
        user_posts=Post.objects.filter(post_user=user.user)
        follwing= UserProfile.objects.filter()
        is_following=None
        followers = user.followers.all()
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
        number_of_followers = len(followers)
        
        
    except Exception as e :
        msg= f'something went wrong {e}'
        return render(request, 'main/not_found.html',{'msg':msg})
    
    
    return render(request, 'accounts/profile.html', {"user":user,'user_posts':user_posts,'number_of_followers':number_of_followers,"is_following":is_following , 'followers':followers})

def add_follower(request:HttpRequest, user_id):
        
            profile = UserProfile.objects.get(id=user_id)
            profile.followers.add(request.user)
            return redirect('accounts:user_profile_view',user_id=profile.user.id)
        
def remove_follower(request:HttpRequest, user_id):
        
            profile = UserProfile.objects.get(id=user_id)
            profile.followers.remove(request.user)
            return redirect('accounts:user_profile_view',user_id=profile.user.id)

def update_user_view(request: HttpRequest):
    msg = None

    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                user : User = request.user
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

              
                profile = UserProfile.objects.get(user=user)
                
                profile.birth_date = request.POST["birth_date"]
                if 'profile_picture' in request.FILES: profile.profile_picture = request.FILES["profile_picture"]
                profile.bio = request.POST["bio"]
                profile.phone_number = request.POST["phone_number"]
                profile.major = request.POST["major"]
                profile.degree = request.POST["degree"]
                profile.university_name = request.POST["university_name"]

                profile.save()

                return redirect("accounts:user_profile_view", user_id = request.user.id)

            else:
                return redirect("accounts:login_user_view")
        except IntegrityError as e:
            msg = f"Please select another username"
        except Exception as e:
            msg = f"something went wrong {e}"

    return render(request, "accounts/update.html", {"msg" : msg})

