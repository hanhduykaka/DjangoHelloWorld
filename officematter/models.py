from django.db import models

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
    user=models.ForeignKey(Clients,on_delete=models.PROTECT)
    roles=models.CharField(
        max_length=2,
        choices=ROLES_CHOICES,
        default=Student
    )
    class Meta:
        db_table = u'ClientsInformation'


