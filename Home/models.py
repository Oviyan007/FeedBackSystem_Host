from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import Count


DESIGNATION_CHOICES = [
            ('FACULTY', 'Faculty'),
            ('STUDENT', 'Student'),
        ]




class User(AbstractUser):
    role =  models.CharField(max_length=10, choices=DESIGNATION_CHOICES, default='STUDENT')


   




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=False,blank=False)
    email = models.EmailField(unique=True, max_length=191, null=False, blank=False)
    password = models.CharField(max_length=50)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES, default='STUDENT',null=False,blank=False)


    def __str__(self):
        return self.name + self.designation

class Batch(models.Model):
    Batchyear=models.CharField(max_length=50,null=False,blank=False)
    department=models.CharField(max_length=50,null=False,blank=False)
    def __str__(self):
        return f" {self.Batchyear}--{self.department}"

SUBJECT_CHOICES=[ ('SUBJECT', 'Subject'),
            ('LABORATORY', 'Laboratory'),]
    
class Subject_detail(models.Model):
    Batch=models.ForeignKey(Batch,on_delete=models.CASCADE,default='')
    sub_code=models.CharField(max_length=50,null=False,blank=False)
    sub_name=models.CharField(max_length=50,null=False,blank=False)
    sub_type=models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='SUBJECT',null=False,blank=False)
    department=models.CharField(max_length=50,default='',null=False,blank=False)
    

    def __str__(self):
        return f" {self.Batch}-------{self.sub_code}---{self.sub_name}"
    
    #staff table 
class Staff(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    staff_id = models.CharField(max_length=20)
    subjects = models.ManyToManyField('Subject_detail', related_name='staff_handling')

    def __str__(self):
        return f"{self.name} ({self.staff_id})"
    
class FeedbackRes(models.Model):
    department = models.CharField(max_length=50)
    Response=models.IntegerField(null=False)
    Qno=models.IntegerField(null=True)
    subject_detail = models.ForeignKey('Subject_detail', on_delete=models.CASCADE, null=True)
    batch_year = models.CharField(max_length=10,null=False)
    
