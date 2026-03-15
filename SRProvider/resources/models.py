from django.db import models
from user_auth.models import CustomUser
import uuid

   
SEM_CHOISES=(
   ('Sem I','SEM I'),
   ('Sem II','SEM II'),
   ('Sem III','SEM III'),
   ('Sem IV','SEM IV'),
   ('Sem V','SEM V'),
   ('Sem VI','SEM VI'),
   ('Sem VII','SEM VII'),
   ('Sem VIII','SEM VIII'),
)


class CourseModel(models.Model):
   user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='cousre_model')
   course_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
   course_name = models.CharField(max_length=250,default='B.Tech CS')
   created_at = models.DateTimeField(auto_now=True)
   
   def __str__(self):
       return self.course_name
    
class SemesterModel(models.Model):
    semester_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    semester = models.CharField(choices=SEM_CHOISES,default='Sem I',max_length=10)
    course = models.ForeignKey(CourseModel,on_delete=models.CASCADE,related_name='semesters')
    
    def __str__(self):
        return f"{self.course.course_name} - {self.semester}"

class Subject(models.Model):
    subject_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    subject_name = models.CharField(max_length=200)
    semester = models.ForeignKey(SemesterModel, on_delete=models.CASCADE, related_name="subjects")

    def __str__(self):
        return self.subject_name
   
class Unit(models.Model):
    unit_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    unit_number = models.PositiveIntegerField()
    unit_title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="units")

    def __str__(self):
        return f"{self.subject.subject_name} - Unit {self.unit_number}: {self.unit_title}"


class Notes(models.Model):
    note_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="notes")   # uploaded file stored in MEDIA_ROOT/notes/
    uploaded_at = models.DateTimeField(auto_now_add=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="notes")

   
   