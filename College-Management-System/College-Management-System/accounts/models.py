from django.db import models

# Create your models here.
class Student_profiles(models.Model):
    firstname = models.CharField(max_length = 200)
    lastname = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    #description = models.TextField()
    class Meta:
        db_table = "student_profiles"
    def __str__(self):
        return self.firstname


class StudentRating(models.Model):
    teacher = models.CharField(max_length=100)
    rating = models.IntegerField()
    username = models.CharField(max_length=100)

    class Meta:
        db_table = "student_rating"

    def __str__(self):
        return f'{self.teacher} - {self.rating}'

class ManagerProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role=models.CharField(max_length=100,default='Manager')
    class Meta:
        db_table = "ManagerProfile"

    def __str__(self):
        return self.username
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)


