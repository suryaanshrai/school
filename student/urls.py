from django.urls import path

from . import views

app_name = "student"

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("check_id/<str:user_id>", views.check_id, name="check_id"),
]