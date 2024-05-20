from django.contrib import admin

from .models import Student, Course

admin.site.register((Student, Course))
