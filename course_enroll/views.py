from math import ceil
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Course

page_limit = 25

def enroll(request, page=1):
    if page <= 0:
        return HttpResponseRedirect(reverse('course_enroll:enroll'))
    pages = ceil(Course.objects.count() / page_limit)
    if page > pages:
        return HttpResponseRedirect(reverse('course_enroll:enroll_page', args=(pages,)))
    all = Course.objects.order_by('name')
    courses = all[(page - 1) * page_limit : page * page_limit]
    params = { 'courses': courses }
    if page > 1:
        params['prev'] = page - 1
    if page < pages:
        params['next'] = page + 1
    return render(request, "enroll.html", params)

def courses(request, id):
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, "courses.html", { "course": course })

def register(request, id):
    pass