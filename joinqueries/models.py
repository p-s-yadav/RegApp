from django.db import models

# Create your models here.
# class College(models.Model):
#     name = models.CharField(max_length=100)
#     department = models.CharField(max_length=100)

# class Student(models.Model):
#     student_name = models.CharField(max_length=100)
#     admitted_to = models.ForeignKey(College, on_delete=models.CASCADE)
#     is_admitted = models.BooleanField(default=True)
#     fees = models.IntegerField()

class College(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    admitted_to = models.ForeignKey(College, on_delete=models.CASCADE, related_name='stu_ad')
    is_admitted = models.BooleanField(default=True)
    fees = models.IntegerField()