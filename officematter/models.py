from django.db import models
from django.contrib.auth.models import User 
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField 
# Create your models here.


class Topic(models.Model):
    top_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.top_name


class WebPage(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.PROTECT)
    name=models.CharField(max_length=200,unique=True)
    url=models.URLField(unique=True)
    image=models.ImageField(upload_to="images/")
    def __str__(self):
        return self.name
class Contents(models.Model):
    name=models.CharField(max_length=200,unique=True)
    # content = RichTextUploadingField()
   
    def __str__(self):
        return self.name
class Clients(models.Model):
    email=models.EmailField(max_length=200,unique=True) 
    username=models.CharField(max_length=200,unique=True)
    password=models.CharField(max_length=200) 
    def __str__(self):
        return self.username

    class Meta:
        db_table = u'Clients'
class ClientsInformation(models.Model):
    Teacher = 'teach'
    Student = 'stu' 
    ROLES_CHOICES = (
        (Teacher, 'Teacher'),
        (Student, 'Student')     
    )
    user_auth = models.OneToOneField(User, on_delete=models.CASCADE)    
    roles=models.CharField(
        max_length=2,
        choices=ROLES_CHOICES,
        default=Student
    )
    bio=models.CharField(max_length=200)


    def __str__(self):
        return self.user_auth.username
    class Meta:
        db_table = u'ClientsInformation'
    
# class Organization(models.Model):
#     Code = models.CharField(max_length=200,unique=True)
#     Manager = models.ForeignKey(User, on_delete=models.PROTECT)    
  
#     bio=models.CharField(max_length=200)


#     def __str__(self):
#         return self.user_auth.username
#     class Meta:
#         db_table = u'ClientsInformation'


