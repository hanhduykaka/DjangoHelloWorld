from django.shortcuts import render
from officematter.models import Topic, WebPage
from officematter.form import FormRegister
from officematter.models import Clients
from datetime import datetime
# Create your views here.


def index(request):
    return render(request, "officematter/index.html")


def about(request):
    userCookie=''
    if '__django__.User' in request.COOKIES:
        userCookie = request.COOKIES['__django__.User']
    return render(request, "officematter/about.html",context={"userCookie":userCookie})


def topicPage(request):
    topiclist = Topic.objects.all().order_by("top_name")
    return render(request, "officematter/topic.html",context= {'topic':topiclist})

def Web_Page(request):
    pagelist = WebPage.objects.all().order_by("name")
    return render(request, "officematter/webpage.html",context= {'pagelist':pagelist})

def register_view(request):  
    form = FormRegister()
    create_date=datetime.now()
    userName=''
    if request.method=='POST':
        form=FormRegister(request.POST,Clients)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['confirm']:
            request.POST._mutable = True
            post = form.save(commit=False)
            post.email=form.cleaned_data['email']
            userName=form.cleaned_data['username']
            post.username = userName
            post.password = form.cleaned_data['password']
            post.save() 
            print("đã insert dư liệu")
        else:
            form.add_error('confirm','form không hợp lệ')
            print('form không hợp lệ')
    response= render(request, "officematter/register.html",{'form':form})
    response.set_cookie('__django__.User',{"username":userName,"create_date":create_date.strftime('%d-%m-%Y %H:%M:%S')})
    return response
