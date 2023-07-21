from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, "home/home.html")


def news(request):
    return render(request, "home/news.html")

def gallery(request):
    return render(request, "home/gallery.html")

def requests(request):
    return render(request, "home/requests.html")

