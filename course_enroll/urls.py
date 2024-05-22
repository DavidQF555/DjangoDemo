from django.urls import path

from . import views

app_name = "course_enroll"
urlpatterns = [
    path("", views.enroll, name="enroll"),
    path("<int:page>", views.enroll, name="enroll_page"),
    path("courses/<int:id>", views.courses, name="courses"),
    path("courses/<int:id>/register", views.register, name="register_course"),
    path("accounts/login", views.account_login, name="login"),
    path("accounts/register", views.account_register, name="register"),
    path("accounts/logout", views.logout, name="logout")
]