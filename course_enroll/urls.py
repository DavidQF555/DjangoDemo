from django.urls import path

from . import views

app_name = "course_enroll"
urlpatterns = [
    path("", views.enroll, name="enroll"),
    path("courses/<int:id>", views.courses, name="courses")
]