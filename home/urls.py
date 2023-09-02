from django.urls import path
from . import views

app_name = "home"

urlpatterns = [    
    path('', views.home, name="home"),
    path("news/", views.news, name="news"),
    path("news_article/<int:news_id>", views.news_article,name="news_article"),
    path("gallery/", views.gallery, name="gallery"),
    path("view_event/<int:event_id>", views.view_event, name="view_event"),
    path("submissions/", views.submissions, name="submissions"),
    path("submissions/<str:message>", views.sub_message, name="sub_message"),
    path("approve/", views.approve, name="approve"),
    path("startnewacademicsession", views.newAcademicSession, name="newAcademicSession"),
]