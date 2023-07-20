from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from .models import User


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponse(f"Logged in as {user.username}")
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
    return HttpResponse("Logged out.")

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
                request, "student/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponse(f"Registered as {user.username}")
    else:
        return render(request, "student/register.html")