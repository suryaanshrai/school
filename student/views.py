from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from .models import User, Result, Schedule, Classroom, Notice, Member
from home.models import Gallery, News
from django.utils import timezone
import csv

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home:home"))
        else:
            return render(
                request,
                "student/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "student/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home:home"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        usergroup = request.POST["usergroup"]
        is_employee=False
        if usergroup == "staff":
            is_employee = True
        if is_employee:
            with open("student/emp_ids.txt", "r") as file:
                if username+"\n" not in file:
                    return render(request, "student/register.html", {
                        "message":"Invalid ID"
                    })
        else:
            with open("student/stud_ids.txt", "r") as file:
                if username+"\n" not in file:
                    return render(request, "student/register.html", {
                        "message":"Invalid ID"
                    })
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "student/register.html", {"message": "Passwords must match."}
            )
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_employee = is_employee
            user.save()
        except IntegrityError:
            return render(
                request, "student/register.html", {"message": "User already register."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("home:home"))
    else:
        return render(request, "student/register.html")


def check_id(request, user_id):
    if request.method == "GET":
        with open("student/stud_ids.txt", "r") as S, open("student/emp_ids.txt","r") as E:
            if user_id+'\n' in S or user_id+'\n' in E:
                return JsonResponse({
                    "is_valid":True
                })
        return JsonResponse({
            "is_valid":False
        })
    return JsonResponse({
        "message":"Invalid Request"
    })


@login_required
def index(request):
    if request.user.is_employee:
        if len(Member.objects.filter(member=request.user)) == 0:
            return HttpResponseRedirect(reverse("student:join_class"))
        class_id = Member.objects.filter(member=request.user)[0].classroom_id
        return HttpResponseRedirect(reverse("student:staff_page", args=[class_id]))
    try:
        user_classroom = Member.objects.get(member=request.user).classroom
    except:
        return HttpResponseRedirect(reverse("student:join_class"))
    schedule = list(Schedule.objects.filter(user=request.user, due_date__gt=timezone.now()).order_by("due_date").values())
    schedule = schedule[:5]
    notices = list(Notice.objects.filter(issued_for=user_classroom).order_by("-id").values())
    notices = notices[:3]
    results = list(Result.objects.filter(student=request.user).order_by("-id").values())
    results = results[:3]
    return render(request, "student/index.html", {
        "schedule":schedule,
        "notices":notices,
        "results":results,
    })

@login_required
def results(request):
    user = User.objects.get(username=request.user)
    all_result = list(Result.objects.filter(student=user).order_by("date").values())
    all_result.reverse()
    return JsonResponse({
        "result":all_result
    })

@login_required
def schedule(request):
    user = User.objects.get(username=request.user)
    min_date = timezone.now()
    schedule = list(Schedule.objects.filter(user=user, due_date__gt=min_date).order_by("due_date").values())
    for item in schedule:
        item["due_date"] = item["due_date"].strftime("%d %b %Y at %H:%M %p")
    return JsonResponse({
        "schedule":schedule
    })

@login_required
def notices(request):
    user = User.objects.get(username=request.user)
    userclass_room = Classroom.objects.get(id=Member.objects.get(member=user).classroom_id)
    notices = list(Notice.objects.filter(issued_for=userclass_room).order_by("-id").values())
    return JsonResponse({
        "notices":notices
    })

@login_required
def user_news(request):
    news=News.objects.filter(author=request.user).order_by("-id")
    return render(request, "student/news.html", {
        "news":news
    })

@login_required
def user_gallery(request):
    gallery=Gallery.objects.filter(author=request.user).order_by("-id")
    return render(request, "student/gallery.html", {
        "gallery":gallery
    })

@login_required
def notice_page(request, notice_id):
    notice=Notice.objects.get(id=notice_id)
    return render(request, "student/notice_page.html", {
        "notice":notice,
    })

@login_required
def add_schedule(request):
    if request.method == "POST":
        new_task=Schedule(user=request.user, activity=request.POST["task"], due_date=request.POST["due_date"])
        new_task.save()
        return HttpResponseRedirect(reverse("student:index"))
    return render(request, "student/schedule.html")

@login_required
def join_class(request):
    if request.method == "POST":
        if not request.user.is_employee:
            try:
                check_class = Member.objects.get(member=request.user)
                return HttpResponse("A student cannot be enrolled in more than one classroom")
            except:
                pass
        standard = request.POST["standard"]
        section = request.POST["section"]
        try:
            classroom = Classroom.objects.get(standard=standard, section=section)
        except:
            return HttpResponse("Invalid Classroom")
        if request.user.is_employee:
            try:
                member=Member.objects.get(member=request.user, classroom=classroom)
                return HttpResponse("Already a member of this class")
            except:
                pass
        new_member = Member(member=request.user, classroom=classroom)
        new_member.save()
        return HttpResponseRedirect(reverse("student:index"))
    return render(request,"student/join_class.html")


@login_required
def staff_page(request, class_id):
    if request.user.is_employee:
        schedule = Schedule.objects.filter(user=request.user, due_date__gt=timezone.now()).order_by("due_date")
        curr_class = Classroom.objects.get(id=class_id)
        emp_classes = Member.objects.filter(member=request.user).order_by("id")
        notices = Notice.objects.filter(issued_for=curr_class).order_by('-id')
        return render(request, "student/index.html", {
            "schedule":schedule,
            "notices":notices,
            "curr_class":curr_class,
            "emp_classes":emp_classes,
        })
    else:
        return HttpResponse("Invalid Access")   
    
@login_required
def create_notice(request, class_id):
    if request.user.is_employee:
        if request.method == "POST":
            new_notice = Notice(issued_for=Classroom.objects.get(id=class_id), issued_by=request.user,
                                title=request.POST["notice_title"], content=request.POST["notice_body"])
            new_notice.save()
            return HttpResponseRedirect(reverse("student:staff_page", args=[class_id]))
        elif request.method == "GET":
            curr_class=Classroom.objects.get(id=class_id)
            return render(request, "student/notice_create.html", {
                "curr_class": curr_class
            })
        
@login_required
def release_score(request, class_id):
    if request.user.is_employee:
        if request.method == "POST":
            curr_class = Classroom.objects.get(id=class_id)
            students = Member.objects.filter(classroom=curr_class)
            max_marks = request.POST["max_marks"]
            date = request.POST["date"]
            topic = request.POST["topic"]
            if request.POST["input_type"] == "manual":
                for student in students:
                    if not student.member.is_employee:
                        s_marks = request.POST["s_"+str(student.member.id)]
                        if s_marks is not None:
                            new_result = Result(student=student.member,topic=topic, marks=s_marks, max_marks=max_marks, date=date)
                            new_result.save()                        
            elif request.POST["input_type"] == "file":
                if 'data_file' in request.FILES:
                    data_file = request.FILES["data_file"]
                    decoded_file=data_file.read().decode('utf-8-sig').splitlines()
                    reader = csv.DictReader(decoded_file)
                    topic = request.POST["topic"]
                    max_marks = request.POST["max_marks"]
                    date = request.POST["date"]
                    for row in reader:
                        student = User.objects.get(username=row["id"])
                        if student not in students:
                            continue
                        marks = row["marks"]
                        new_result=Result(student=student, topic=topic, marks=marks, max_marks=max_marks, date=date)
                        new_result.save()
                else:
                    return HttpResponse("Invalid File Upload")
            return HttpResponseRedirect(reverse('student:staff_page', args=[class_id]))
        elif request.method == "GET":
            curr_class = Classroom.objects.get(id=class_id)
            students = Member.objects.filter(classroom=curr_class)
            return render(request, "student/score_release.html", {
                "curr_class":curr_class,
                "students":students,
            })
        
@login_required
def add_schedule_class(request,class_id):
    if request.user.is_employee:
        if request.method == "POST":
            classroom = Classroom.objects.get(id=class_id)
            students = Member.objects.filter(classroom=classroom)
            for student in students:
                new_schedule = Schedule(user=student.member, activity=request.POST["task"], due_date=request.POST["due_date"])
                new_schedule.save()
            return HttpResponseRedirect(reverse("student:index"))
        elif request.method == "GET":
            classroom = Classroom.objects.get(id=class_id)
            return render(request, "student/schedule_class.html", {
                "class":classroom
            })
    else:
        return HttpResponse("Invalid Access")