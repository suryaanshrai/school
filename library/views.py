from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from student.models import User
from .models import Book, Issue, Request, Penalty

@login_required
def index(request):
    s=User.objects.get(username=request.user).username
    if s == "librarian":
        isLibrarian = True
    else:
        isLibrarian = False
    books_issued = Issue.objects.filter(user=request.user)
    return render(request, "library/index.html", {
        "isLibrarian":isLibrarian,
        "books_issued":books_issued,
    })

def search(request):
    if request.method == "GET":
        q = request.GET["q"]
        res = list(Book.objects.filter(name__contains=q).filter(author__contains=q).values())        
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