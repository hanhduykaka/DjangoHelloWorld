from django.shortcuts import render
from officematter.models import Topic, WebPage
from officematter.form import FormRegister,UserForm,UserProfileInfoForm
from officematter.models import Clients
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
# Create your views here.

@login_required(login_url='/login')
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
    registered = False
    if request.method=='POST':
        form_user = UserForm(data=request.POST)
        form_por = UserProfileInfoForm(data = request.POST)
        if form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']:
            request.POST._mutable = True
            user = form_user.save()
            user.set_password(user.password)
            user.save()
            profile = form_por.save(commit = False)
            profile.user_auth = user            
            profile.save()
            registered = True
            print("đã insert dư liệu")
            username = request.POST['username']
            password = request.POST['password']
            #authenticate user then login
            user_authenticate = authenticate(username=username, password=password)
            login(request, user_authenticate)
            return HttpResponseRedirect('/office-master/')
        else:
            form_user.add_error('confirm','form không hợp lệ')
            print(form_user.errors, form_por.errors)
    else:
        form_user = UserForm()
        form_por = UserProfileInfoForm() 
        return render(request, "officematter/register.html", {'user_form':form_user,\
 'profile_form': form_por,
 'registered': registered})

    # response= render(request, "officematter/register.html",{'form':form})
    # response.set_cookie('__django__.User',{"username":userName,"create_date":create_date.strftime('%d-%m-%Y %H:%M:%S')})
    # return response
def login_view(request):
    if request.method=='POST':        
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password = password)
        if user:
            if user.is_active:
                login(request, user)                
                return HttpResponseRedirect('/office-master/')
            else:
                print("Không đăng nhập được")
                print("Username: {} and password: {}".format(username, password))
                login_result = "Username và password không hợp lệ"
                return render(request, "officematter/login.html",{"login_result", login_result})
   
    return render(request, "officematter/login.html")

@login_required
def user_logout(request):
     logout(request)
     return HttpResponseRedirect('/office-master/login')



 

     

