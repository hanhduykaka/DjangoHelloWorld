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

class Type(models.Model):
    Name=models.CharField(max_length=200,unique=True) 

    def __str__(self):
        return self.Name
    class Meta:
        db_table = u'Type'
        
class Organization(models.Model):  
    Name = models.CharField(max_length=200,unique=True)  
    Manager = models.ForeignKey(User, on_delete=models.PROTECT)
    Type = models.ForeignKey(Type, on_delete=models.PROTECT)
    IsPublic= models.BooleanField()
    Purpose = models.CharField(max_length=200)    
    Image=models.ImageField(default='images/favicon.ico',blank=True, null=True,upload_to="images/")
    def __str__(self):
        return self.Name
    class Meta:
        db_table = u'Organization'

class OrganizationMember(models.Model):    
    ClientId = models.ForeignKey(User, on_delete=models.PROTECT)
    OrgId = models.ForeignKey(Organization, on_delete=models.PROTECT)   

    class Meta:
        db_table = u'OrganizationMember'

class Achievement(models.Model):
    Achievement = models.ImageField(upload_to="images/")
    Success = models.BooleanField()
    Date= models.DateField()
    ClientId = models.ForeignKey(User, on_delete=models.PROTECT)
    OrgId = models.ForeignKey(Organization, on_delete=models.PROTECT)

    class Meta:
        db_table = u'Achievement'



    
