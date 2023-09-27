from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from student.models import User
from .models import Book, Issue, Penalty
from datetime import date
import csv



@login_required
def index(request):
    s=User.objects.get(username=request.user).username
    if s == "librarian":
        isLibrarian = True
    else:
        isLibrarian = False
    books_issued = Issue.objects.filter(user=request.user)
    penalties = Penalty.objects.filter(user=request.user)
    total_penalty = 0
    for penalty in penalties:
        total_penalty += penalty.amount
    return render(request, "library/index.html", {
        "isLibrarian":isLibrarian,
        "books_issued":books_issued,
        "penalties":penalties,
        "total_penalty":total_penalty,
    })

def search(request):
    if request.method == "GET":
        q = request.GET["q"]
        print(q)
        names = list(Book.objects.filter(name__contains=q).values()) 
        author = list(Book.objects.filter(author__contains=q).values())          
        res = names
        for x in author:
            if x not in res:
                res += [x]
        s=User.objects.get(username=request.user).username
        res_u = list()
        if s == "librarian":
            try:
                res_u = list(Issue.objects.filter(user=User.objects.get(username=q)).values())
                for obj in res_u:
                    obj["book_name"] = Book.objects.get(id=obj["book_id"]).name
                    obj["username"] = User.objects.get(id=obj["user_id"]).username
            except:
                pass
        return JsonResponse({
            "res":res,
            "res_u":res_u,
            })
    

@login_required
def issue(request):
    if request.method == "POST":
        s = User.objects.get(username=request.user).username
        if s == "librarian":
            student = User.objects.get(username=request.POST["student_id"])
            book =  Book.objects.get(id=int(request.POST["book_id"]))
            if book.quantity == 0:
                return JsonResponse({
                    "message":"Book unavailable"
                })
            if len(Issue.objects.filter(book=book,user=student)) == 0:
                Issue(book=book,user=student).save()
                book.quantity = book.quantity - 1
                book.save()
                return JsonResponse({
                    "message":"Book Issued"
                })
            else:
                issue = Issue.objects.get(book=book,user=student)
                diff = date.today() - issue.due_date
                issue.delete()
                penalty = 0
                if diff.days > 0:
                    penalty = diff.days*2
                book.quantity = book.quantity + 1
                book.save()
                return JsonResponse({
                    "message":f"Book Returned. Penalty accrued: Rs. {penalty}"
                })
        else:
            return JsonResponse({
                    "message":"Invalid Access"
                })
    else:
        return JsonResponse({
                    "message":"Invalid Request"
                })
    

@login_required
def penalty(request, username):
    if request.method == "POST":
        s = User.objects.get(username=request.user).username
        if s == "master":
            penalty = Penalty.objects.get(id=request.POST["penalty_id"])
            penalty.delete()
            return HttpResponseRedirect(reverse('library:penalty', args=[username]))
        else:
            return HttpResponse("Invalid Access")
    elif request.method == "GET":
        s = User.objects.get(username=request.user).username
        if s == "librarian":
            penalties = Penalty.objects.filter(user=User.objects.get(username=username))
            return render(request,"library/penalties.html",{
                "penalties":penalties,
                "user":username,
            })
        else:
            return HttpResponse("Invalid Access")
        
@login_required
def penalty_form(request):
    if request.method == "POST":
        s = User.objects.get(username=request.user).username
        if s == "librarian":
            user = request.POST["student_id"]
            return HttpResponseRedirect(reverse('library:penalty', args=[user]))
        else:
            return HttpResponse("Inavlid Access")
    else:
        return HttpResponse("Invalid request")
    

@login_required
def add_book(request):
    if request.method == "POST":
        s = User.objects.get(username=request.user).username
        if s == "librarian":
            book_name = request.POST["book_name"]
            author_name = request.POST["author_name"]
            quantity = int(request.POST["quantity"])
            book_q = Book.objects.filter(name__contains=book_name,author__contains=author_name)
            if len(book_q) == 0:
                new_book = Book(name=book_name,author=author_name,quantity=quantity)
                new_book.save()
            else:
                book_q[0].quantity += quantity
                book_q[0].save()
            return JsonResponse({
                    "message":"Book added successfully",
                })
        else:
            return JsonResponse({
                    "message":"Inavlid access",
                })
    return JsonResponse({
                    "message":"Invalid request",
                })



@login_required
def add_book_csv(request):
    if request.method == "POST":
        s = User.objects.get(username=request.user).username
        if s == "librarian":
            if "book_list" in request.FILES:
                book_list = request.FILES["book_list"]
                decoded_file=book_list.read().decode('utf-8-sig').splitlines()
                reader = csv.DictReader(decoded_file)
                print(decoded_file)
                for row in reader:
                    book_name = row['book_name']
                    author_name = row['author_name']
                    quantity = int(row['quantity'])
                    book_q = Book.objects.filter(name__iexact=book_name,author__iexact=author_name)
                    if len(book_q) == 0:
                        new_book = Book(name=book_name,author=author_name,quantity=quantity)
                        new_book.save()
                    else:
                        book_q[0].quantity += quantity
                        book_q[0].save()
                return JsonResponse({
                    "message":"All books added",
                })
        return JsonResponse({
                    "message":"Invalid access",
                })
    return JsonResponse({
                    "message":"Invalid request",
                })