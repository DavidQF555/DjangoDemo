from math import ceil
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as lo
from django.contrib import messages
from .models import Course, Student

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
    params['auth'] = request.user.is_authenticated
    return render(request, "enroll.html", params)

def courses(request, id):
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    count = Student.objects.filter(courses__in=[id]).count()
    params = { "course": course, "count": count, 'auth': request.user.is_authenticated, "in_course": False }
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(user=request.user)
            params["in_course"] = student.courses.filter(id=id).exists()
        except Student.DoesNotExist:
            pass
    return render(request, "courses.html", params)

def register_course(request, id):
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                student = Student.objects.get(user_id=request.user.id)
            except Student.DoesNotExist:
                messages.add_message(request, messages.ERROR, "Not a student.")
                return HttpResponseRedirect(reverse('course_enroll:courses', args=(id,)))
            if student.courses.filter(id=id).exists():
                messages.add_message(request, messages.ERROR, "Already enrolled.")
                return HttpResponseRedirect(reverse('course_enroll:courses', args=(id,)))
            count = Student.objects.filter(courses__in=[id]).count()
            if count >= course.capacity:
                messages.add_message(request, messages.ERROR, "Course full.")
                return HttpResponseRedirect(reverse('course_enroll:courses', args=(id,)))
            student.courses.add(course)
            student.save()
            messages.add_message(request, messages.SUCCESS, "Successfully enrolled.")
        else:
            messages.add_message(request, messages.ERROR, "Must be logged in.")
    return HttpResponseRedirect(reverse('course_enroll:courses', args=(id,)))

def leave_course(request, id):
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                student = Student.objects.get(user_id=request.user.id)
            except Student.DoesNotExist:
                messages.add_message(request, messages.ERROR, "Not a student.")
                return HttpResponseRedirect(reverse('course_enroll:courses', args=(id,)))
            if not student.courses.filter(id=id).exists():
                messages.add_message(request, messages.ERROR, "Not enrolled.")
                return HttpResponseRedirect(reverse('course_enroll:courses', args=(id,)))
            student.courses.remove(course)
            student.save()
            messages.add_message(request, messages.SUCCESS, "Successfully left.")
        else:
            messages.add_message(request, messages.ERROR, "Must be logged in.")
    return HttpResponseRedirect(reverse('course_enroll:courses', args=(id,)))

def enrolled(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, "Must be logged in.")
        return HttpResponseRedirect(reverse('course_enroll:courses'))
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Not a student.")
        return HttpResponseRedirect(reverse('course_enroll:courses'))
    return render(request, "enrolled.html", { 'courses': student.courses.all() })

def account_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            messages.add_message(request, messages.ERROR, "Please fill out all fields.")
            return HttpResponseRedirect(reverse("course_enroll:login"))
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.add_message(request, messages.ERROR, "Invalid login.")
            return HttpResponseRedirect(reverse("course_enroll:login"))
        login(request=request, user=user)
        messages.add_message(request, messages.SUCCESS, "Successfully logged in.")
        return HttpResponseRedirect(reverse("course_enroll:enroll"))
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("course_enroll:enroll"))
    return render(request, "accounts/login.html")

def account_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            messages.add_message(request, messages.ERROR, "Please fill out all fields.")
            return HttpResponseRedirect(reverse("course_enroll:register"))
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "There is already a user with the same username.")
            return HttpResponseRedirect(reverse("course_enroll:register"))
        user = User.objects.create_user(username=username, password=password)
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        messages.add_message(request, messages.SUCCESS, "Successfully registered. Please login.")
        return HttpResponseRedirect(reverse("course_enroll:register"))
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("course_enroll:enroll"))
    return render(request, "accounts/register.html")

def logout(request):
    lo(request)
    messages.add_message(request, messages.SUCCESS, "Successfully logged out.")
    return HttpResponseRedirect(reverse("course_enroll:enroll"))