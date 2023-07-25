from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from student.models import User
from .models import News,Event,Gallery,ActiveSession
# Create your views here.

def home(request):
    return render(request, "home/home.html")

def is_image(file: UploadedFile) -> bool:
    content_type = file.content_type
    return content_type.startswith("image/")

@login_required
def submissions(request):
    # receive and validate submissions (validate that the file is an image)
    # if a user is an employee return all the submissions in chronological order with the option to approve or reject the submission
    if request.method == "POST":
        sub_type=request.POST["sub_type"]
        if sub_type == "news":
            print("News")
        elif sub_type == "gallery":
            title = request.POST["title"]
            image = request.FILES["image"]
            if not image.content_type.startswith("image/"):
                return render(request,"home/submissions.html", {"message":"Uploaded file is not an image!"})
            elif image.size > 3145728:
                return render(request,"home/submissions.html", {"message":"Image larger than 3MB!"})
            author = User.objects.get(username=request.user)
            event_id = int(request.POST["event"])
            if event_id != 0:
                event = Event.objects.get(id=event_id)
                new_image = Gallery(image=image,title=title, author=author, event=event)
                new_image.save()
            else:
                new_image = Gallery(image=image,title=title, author=author)
                new_image.save()
        elif sub_type == "event":
            print("New Event!")
        else:
            return render(request,"home/submissions.html", {
                "message":"Invalid Data :("
            })
    gallery_subs=Gallery.objects.filter(approved_by=None)
    news_subs = News.objects.filter(approved_by=None)
    return render(request, "home/submissions.html", {
        "message":"",
        "gallery_subs":gallery_subs,
        "news_subs":news_subs,
    })

def news(request):
    return render(request, "home/news.html")

def gallery(request):
    gallery_subs=Gallery.objects.exclude(approved_by=None)
    return render(request, "home/gallery.html", {
        "gallery_subs":gallery_subs,
    })

def requests(request):
    return render(request, "home/requests.html")

@login_required
def approve(request):
    if request.method == "POST":
        if not request.user.is_employee:
            return HttpResponseRedirect(reverse('home:submissions'), {"message":"Unauthorized Request"})
        if request.POST["verdict"] == "Approve":
            gal_obj = Gallery.objects.get(id=int(request.POST["sub_id"]))
            gal_obj.approved_by = User.objects.get(username=request.user)
            gal_obj.save()
    return HttpResponseRedirect(reverse('home:submissions'))

@login_required
def events(request):
    if request.user.is_employee:
        if request.method == "POST":
            pass
        return render(request, "home/events.html")
    return HttpResponse("Invalid Access Request")