from django.urls import path
from . import views

app_name="library"

urlpatterns=[
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("issue", views.issue, name="issue"),
    path("penalty/<str:username>", views.penalty, name="penalty"),
    path("penaltyform", views.penalty_form, name="penaltyform"),
    path("add_book", views.add_book, name="add_book"),
    path("add_book_csv", views.add_book_csv, name="add_book_csv"),
]