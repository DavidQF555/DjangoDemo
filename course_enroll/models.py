from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField()
    capacity = models.IntegerField()
    enrolled = models.IntegerField(default=0)

class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)