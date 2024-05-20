from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import Course

def enroll(request):
    return render(request, "enroll.html")

def courses(request, id):
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, "courses.html", { "course": course })