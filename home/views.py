from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, "home/home.html")


@login_required
def submissions(request):
    # receive and validate submissions (validate that the file is an image)
    # if a user is an employee return all the submissions in chronological order with the option to approve or reject the submission
    if request.method == "POST":
        pass
    return render(request, "home/submissions.html", {
        "message":""
    })


def news(request):
    return render(request, "home/news.html")

def gallery(request):
    return render(request, "home/gallery.html")

def requests(request):
    return render(request, "home/requests.html")

