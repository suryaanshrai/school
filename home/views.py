from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from student.models import User
from .models import News,Event,Gallery
from django.utils import dateparse
from datetime import datetime

def home(request):
    return render(request, "home/home.html")


@login_required
def submissions(request):
    """
    Receive requests for News articles and images for gallery and allow signed in employees to 
    create new events for the Gallery
    """
    if request.method == "POST":
        sub_type=request.POST["sub_type"] 
        if sub_type == "news": 
            return handle_news(request)
        elif sub_type == "gallery": 
            return handle_gallery(request)
        elif sub_type == "event": 
            return handle_event(request)
        else:
            return render(request,"home/submissions.html", {
                "message":"Invalid Data :("
            })
        
    gallery_subs=Gallery.objects.filter(approved_by=None)
    news_subs = News.objects.filter(approved_by=None)
    event_list = Event.objects.all()
    return render(request, "home/submissions.html", {
        "message":"",
        "events":event_list,
        "gallery_subs":gallery_subs,
        "news_subs":news_subs,
    })

@login_required
def sub_message(request,message):
    gallery_subs=Gallery.objects.filter(approved_by=None)
    news_subs = News.objects.filter(approved_by=None)
    event_list = Event.objects.all()
    return render(request, "home/submissions.html", {
        "message":message,
        "events":event_list,
        "gallery_subs":gallery_subs,
        "news_subs":news_subs,
    })

@login_required
def approve(request):
    """Handles approval or rejection of a News or Gallery request"""
    if request.method == "POST":
        if not request.user.is_employee:
            return render(request,'home/submissions.html', {"message":"Unauthorized request!"})
        if request.POST["sub_type"] == "gallery":
            gal_obj = Gallery.objects.get(id=int(request.POST["sub_id"]))
            if request.POST["verdict"] == "Approve":
                try:
                    gal_obj.event = Event.objects.get(id=int(request.POST["event"]))
                except ObjectDoesNotExist:
                    return HttpResponseRedirect(reverse('home:sub_message', args=["Gallery Image needs to be assigned an event!"]))
                gal_obj.approved_by = User.objects.get(username=request.user)
                gal_obj.save()
                return HttpResponseRedirect(reverse('home:sub_message', args=["Image accepted for gallery"]))
            elif request.POST["verdict"] == "Reject":
                gal_obj.delete()
                return HttpResponseRedirect(reverse('home:sub_message', args=["Rejected image for gallery"]))
        elif request.POST["sub_type"] == "news":
            news_obj = News.objects.get(id=int(request.POST["sub_id"]))
            if request.POST["verdict"] == "Approve":
                news_obj.approved_by = User.objects.get(username=request.user)
                news_obj.active = True
                news_obj.save()
                return HttpResponseRedirect(reverse('home:sub_message', args=["Approved news article"]))
            elif request.POST["verdict"] == "Reject":
                news_obj.delete()
                return HttpResponseRedirect(reverse('home:sub_message', args=["Rejected news article"]))
        else:
            return HttpResponseRedirect(reverse('home:sub_message', args=["Invalid Request"]))
    return HttpResponseRedirect(reverse('home:submissions'))


def view_event(request,event_id):
    images = Gallery.objects.filter(event_id=event_id).exclude(approved_by=None)
    event_name = Event.objects.get(id=event_id).event_name
    return render(request, "home/gallery.html", {
        "images":images,
        "event_name":event_name,
    })

def gallery(request):
    """Manages the gallery section"""
    gal_events = Event.objects.filter(active=True).order_by('-date')
    arch_events = Event.objects.filter(active=False).order_by('-date')
    return render(request, "home/gallery.html", {
        "gal_events":gal_events,
        "arch_events":arch_events,
    })


def news(request):
    """Manages the News Section"""
    news_subs = News.objects.filter(active=True).order_by('-date')
    archived_news = News.objects.exclude(approved_by=None).exclude(active=True).order_by('-date') 
    return render(request, "home/news.html", {
        "news_subs":news_subs,
        "archived_news":archived_news,
    })

def news_article(request, news_id):
    try:
        article=News.objects.get(id=news_id)
    except ObjectDoesNotExist:
        return HttpResponse("Invalid Request")
    return render(request, "home/news.html",{
        "article":article
    })

def valid_image(image):
    """Checks if the given file is a valid image or not"""
    if not image.content_type.startswith("image/"):
        return "Uploaded file is not an image!"
    elif image.size > 3145728:
        return "Image larger than 3MB!"
    return True

def handle_news(request):
    """Handles news article request"""
    print("something happened")
    title = request.POST["title"]
    date = request.POST["date"]
    description=request.POST["description"]
    author = User.objects.get(username=request.user)
    if dateparse.parse_datetime(date) > datetime.now():
        return HttpResponseRedirect(reverse('home:sub_message', args=["Date of event cannot be in the future!"]))
    try:
        image = request.FILES["image"]
    except MultiValueDictKeyError:
        image = None
    if image is not None:
        if valid_image(image) != True:
            return HttpResponseRedirect(reverse('home:sub_message', args=[valid_image(image)]))
        News(title=title,date=date,image=image,description=description, author=author).save()
    else:
        News(title=title,date=date,description=description, author=author).save()
    return HttpResponseRedirect(reverse('home:sub_message', args=["News article received. Thank you for your contribution!"]))


def handle_gallery(request):
    """Handles gallery requests"""
    title = request.POST["title"]
    image = request.FILES["image"]
    if valid_image(image) != True:
        print(valid_image(image))
        return HttpResponseRedirect(reverse('home:sub_message', args=[valid_image(image)]))
    author = User.objects.get(username=request.user)
    event_id = int(request.POST["event"])
    if event_id != 0:
        event = Event.objects.get(id=event_id)
        new_image = Gallery(image=image,title=title, author=author, event=event)
        new_image.save()
    else:
        new_image = Gallery(image=image,title=title, author=author)
        new_image.save()
    return HttpResponseRedirect(reverse('home:sub_message', args=["Image submission received. Thank you for your contribution!"]))

def handle_event(request):
    """Handles creation of new events"""
    if not request.user.is_employee:
        return HttpResponseRedirect(reverse('home:sub_message', args=["Unauthorized Request"]))
    event_name=request.POST["event_name"]
    event_date=request.POST["event_date"]
    if dateparse.parse_datetime(event_date) > datetime.now():
        return HttpResponseRedirect(reverse('home:sub_message', args=["Date of event cannot be in the future!"]))
    Event(event_name=event_name,date=event_date, active=True).save()
    return HttpResponseRedirect(reverse('home:sub_message', args=["Event saved successfully"]))