from django.urls import path
from . import views

app_name = "home"

urlpatterns = [    
    path('', views.home, name="home"),
    path("news/", views.news, name="news"),
    path("gallery/", views.gallery, name="gallery"),
    path("request/", views.requests, name="requests"),
    path("submissions/", views.submissions, name="submissions"),
    path("approve/", views.approve, name="approve"),
    path("events/", views.events, name="events"),
]