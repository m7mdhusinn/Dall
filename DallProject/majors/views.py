from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from certificates.models import Certificate
from companies.models import Company
from courses.models import Course
from jobs.models import Job
from skills.models import Skill
from .models import Major
from favorites.models import Favorite

# Create your views here.

def add_major_view(request:HttpRequest):
    msg=None
    try:
        if request.method == "POST":
            new_major= Major(name=request.POST["name"],
                                    description=request.POST["description"],
                                    )
            if 'image' in request.FILES:
                new_major.image=request.FILES["image"]

            new_major.save()
            return redirect('majors:major_home_view')
    except Exception as e:
        msg = f"An error occured, please fill in all fields and try again . {e}"
    return render(request , 'majors/add_major.html',{'msg':msg})

def update_major_view(request:HttpRequest,major_id):
    msg=None
    try:
        update_major=Major.objects.get(id=major_id)
        
        if request.method == "POST":
            update_major.name=request.POST["name"]
            update_major.description=request.POST["description"]
            if 'image' in request.FILES:
                update_major.image=request.FILES["image"]

            update_major.save()
            return redirect ('majors:detail_major_view',major_id=update_major.id)
    except Exception as e:
        msg = f"An error occured, please fill in all fields and try again . {e}"
            
    return render(request, 'majors/update_major.html',{"update_major":update_major,'msg':msg})
def delete_major_view(request:HttpRequest,major_id):
    try:
        delete_major=Major.objects.get(id=major_id)
        
        delete_major.delete()
        return redirect('majors:detail_major_view')
    except Exception as e:
         msg = f"An error occured, please fill in all fields and try again . {e}"
    return render(request, 'majors/detail_major.html',{"msg":msg})
def major_home_view(request:HttpRequest):
    try:
        keyword=None
        if "search" in request.GET:
            keyword =request.GET.get("search")
            view_major = Major.objects.filter(name__contains=keyword)
        else:    
            view_major=Major.objects.all()

    except:
        return render(request, "main/not_found.html", status=401)
    return render(request , 'majors/major_home.html',{'view_major':view_major, 'keyword':keyword})
def detail_major_view(request:HttpRequest,major_id):
    
    major_detail=Major.objects.get(id=major_id)
    certificates = Certificate.objects.exclude(major=major_detail)
    companies = Company.objects.exclude(major=major_detail)
    courses = Course.objects.exclude(major=major_detail)
    jobs = Job.objects.exclude(major=major_detail)
    skills = Skill.objects.exclude(major=major_detail)
    is_favored = request.user.is_authenticated and Favorite.objects.filter(major=major_detail, user=request.user).exists()

    return render(request, 'majors/detail_major.html',{"major_detail":major_detail,'certificates':certificates,'companies':companies,'courses':courses,"jobs":jobs,'skills':skills,'is_favored':is_favored})