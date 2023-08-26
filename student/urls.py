from django.urls import path

from . import views

app_name = "student"

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("check_id/<str:user_id>", views.check_id, name="check_id"),
    path("", views.index, name="index"),
    path("results", views.results, name="results"),
    path("schedule", views.schedule, name="schedule"),
    path("notices", views.notices, name="notices"),
    path("user_news", views.user_news, name="user_news"),
    path("user_gallery", views.user_gallery, name="user_gallery"),
    path("notice_page/<int:notice_id>", views.notice_page, name="notice_page"),
    path("add_schedule", views.add_schedule, name="add_schedule"),
    path("join_class", views.join_class, name="join_class"),
    path("staff_page/<int:class_id>", views.staff_page, name="staff_page"),
    path("create_notice/<int:class_id>", views.create_notice, name="create_notice"),
    path("release_score/<int:class_id>", views.release_score, name="release_score"),
    path("add_schedule_class/<int:class_id>", views.add_schedule_class, name="add_schedule_class"),
]