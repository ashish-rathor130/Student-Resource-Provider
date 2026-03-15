from django.contrib import admin
from .models import CourseModel,SemesterModel,Subject,Unit,Notes

admin.site.register([CourseModel,SemesterModel,Subject,Unit,Notes])