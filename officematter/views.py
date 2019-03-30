from django.shortcuts import render
from officematter.models import Topic, WebPage, Organization, Type ,OrganizationMember
from officematter.form import FormRegister, UserForm, UserProfileInfoForm, TopicsForm, OrganizationForm,OrganizationMemberForm
from officematter.models import Clients, User
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json
import urllib
from .serialize import TopicSerializer, OrganizationSerializer, UserSerializer, TypeSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Q
# Create your views here.


@login_required(login_url='/login')
def index(request):
    url = "http://127.0.0.1:8000/api/v2/organizations"
    default_encoding = 'utf-8'
    url_response = urllib.request.urlopen(url)

    if hasattr(url_response.headers, 'get_content_charset'):
        encoding = url_response.headers.get_content_charset(default_encoding)
    else:
        encoding = url_response.headers.getparam('charset') or default_encoding
    data = json.loads(url_response.read().decode(encoding))  
    org_member= OrganizationMember.objects.filter(ClientId=request.user.pk)
    org_list = list(org_member.values('OrgId'))
    ore_list_string =', '.join(str(d['OrgId']) for d in org_list)
    if request.user.is_superuser:
        data=data
    else:
        data=[d for d in data if( (d['IsPublic'] == True or d['Manager']['username']==request.user.username or str(d['id']) in ore_list_string) ) ]
    return render(request, "officematter/index.html",context={'org_lists': data,'org_member':org_list})

@login_required(login_url='/login')
def about(request):
    userCookie = ''
    if '__django__.User' in request.COOKIES:
        userCookie = request.COOKIES['__django__.User']
    return render(request, "officematter/about.html", context={"userCookie": userCookie})


def topicPage(request):
    topiclist = Topic.objects.all().order_by("top_name")
    return render(request, "officematter/topic.html", context={'topic': topiclist})


def topicPageGetFromAPI_V2(request):
    url = "http://127.0.0.1:8000/api/v2/topics"
    default_encoding = 'utf-8'
    url_response = urllib.request.urlopen(url)

    if hasattr(url_response.headers, 'get_content_charset'):
        encoding = url_response.headers.get_content_charset(default_encoding)
    else:
        encoding = url_response.headers.getparam('charset') or default_encoding
    data = json.loads(url_response.read().decode(encoding))
    print(data)
    return render(request, "officematter/topic.html", context={'topic': data})


def Web_Page(request):
    pagelist = WebPage.objects.all().order_by("name")
    return render(request, "officematter/webpage.html", context={'pagelist': pagelist})


def register_view(request):
    registered = False
    if request.method == 'POST':
        form_user = UserForm(data=request.POST)
        form_por = UserProfileInfoForm(data=request.POST)
        if form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']:
            request.POST._mutable = True
            user = form_user.save()
            user.set_password(user.password)
            user.save()
            profile = form_por.save(commit=False)
            profile.user_auth = user
            profile.save()
            registered = True
            print("đã insert dư liệu")
            username = request.POST['username']
            password = request.POST['password']
            # authenticate user then login
            user_authenticate = authenticate(
                username=username, password=password)
            login(request, user_authenticate)
            return HttpResponseRedirect('/office-master/')
        else:
            form_user.add_error('confirm', 'form không hợp lệ')
            print(form_user.errors, form_por.errors)
            return render(request, "officematter/register.html", {'user_form': form_user,
                                                                  'profile_form': form_por,
                                                                  'registered': registered})
    else:
        form_user = UserForm()
        form_por = UserProfileInfoForm()
        return render(request, "officematter/register.html", {'user_form': form_user,
                                                              'profile_form': form_por,
                                                              'registered': registered})

    # response= render(request, "officematter/register.html",{'form':form})
    # response.set_cookie('__django__.User',{"username":userName,"create_date":create_date.strftime('%d-%m-%Y %H:%M:%S')})
    # return response


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/office-master/')
    elif request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/office-master/')
            else:
                print("Không đăng nhập được")
                print("Username: {} and password: {}".format(username, password))
                login_result = "Username và password không hợp lệ"
                return render(request, "officematter/login.html", {"login_result", login_result})

    return render(request, "officematter/login.html")


def get_list_users(request):
    userObjects = User.objects.order_by('username')
    lstUser = list(userObjects.values('username', 'email'))
    return HttpResponse(json.dumps(lstUser, ensure_ascii=False).encode('utf8'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/office-master/login')


def User_views(request):
    url = "http://127.0.0.1:8000/api/v1/users"
    default_encoding = 'utf-8'
    url_response = urllib.request.urlopen(url)

    if hasattr(url_response.headers, 'get_content_charset'):
        encoding = url_response.headers.get_content_charset(default_encoding)
    else:
        encoding = url_response.headers.getparam('charset') or default_encoding
    data = json.loads(url_response.read().decode(encoding))
    return HttpResponse(data)


@csrf_exempt
def restAPI_Topics(request):
    if request.method == "GET":
        _topic = Topic.objects.all()
        serializer = TopicSerializer(_topic, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TopicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def topic_create_view(request):
    if request.method == 'POST':
        form_topic = TopicsForm(data=request.POST)
        if form_topic.is_valid():
            request.POST._mutable = True
            topic = form_topic.save()
            topic.save()
            print("đã insert dư liệu")
            return HttpResponseRedirect('/topic-from-api')
        else:
            return render(request, "officematter/topic_create.html", {'form_topic': form_topic})
    else:
        form_topic = TopicsForm()
        return render(request, "officematter/topic_create.html", {'form_topic': form_topic})


# api create && get all Organization
@csrf_exempt
def restAPI_Organizations(request):
    if request.method == "GET":
        _org = Organization.objects.all()
        serializer = OrganizationSerializer(_org, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = OrganizationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    


@csrf_exempt
def restAPI_Organization_Details(request, pk):
    try:
        _org = Organization.objects.get(pk=pk)
    except _org.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = OrganizationSerializer(_org)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = OrganizationSerializer(_org, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        _org.delete()
        return JsonResponse(serializer.data, status=200)

@login_required(login_url='/login')
def org_create_view(request):
    if request.method == 'POST':             
        form_org = OrganizationForm(request.POST, request.FILES)            
        if form_org.is_valid():
            request.POST._mutable = True            
            org = form_org.save(commit=False)
            if request.user.is_superuser:
                org.Manager =org.Manager
            else:
                org.Manager = request.user 
            org.save()
            print("đã insert dư liệu")
            return HttpResponseRedirect('/organization-list')
        else:
            return render(request, "officematter/org_create.html", {'form_org': form_org})
    else:
        form_org = OrganizationForm()
        return render(request, "officematter/org_create.html", {'form_org': form_org})

@login_required(login_url='/login')
def org_lists(request):
    url = "http://127.0.0.1:8000/api/v2/organizations"
    default_encoding = 'utf-8'
    url_response = urllib.request.urlopen(url)

    if hasattr(url_response.headers, 'get_content_charset'):
        encoding = url_response.headers.get_content_charset(default_encoding)
    else:
        encoding = url_response.headers.getparam('charset') or default_encoding
    data = json.loads(url_response.read().decode(encoding))
    print(data)
    return render(request, "officematter/org_lists.html", context={'org_lists': data})

@login_required(login_url='/login')
def org_detail_view(request, pk, template_name='officematter/org_detail.html'):
    org= get_object_or_404(Organization, pk=pk)
    form = OrganizationForm(instance=org)
    return render(request, template_name, context={'form': form})

@login_required(login_url='/login')
def org_detail_edit(request, pk=None, template_name="officematter/org_create.html"):
    org = get_object_or_404(Organization, pk=pk)
    if request.method == "POST":
        form = OrganizationForm(request.POST or None,request.FILES or None, instance=org)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/organization-list')
        else:
            return render(request, template_name, {'form_org': form})
    else:
        form = OrganizationForm(instance=org)
        print(form)
        return render(request, template_name, {'form_org': form})

@login_required(login_url='/login')       
def org_delete(request, pk, template_name='officematter/org_confirm_delete.html'):
    org= get_object_or_404(Organization, pk=pk)    
    if request.method=='POST':
        org.delete()
        return HttpResponseRedirect('/organization-list')
    return render(request, template_name, {'object':org})

@login_required(login_url='/login')       
def org_add_member(request, pk, template_name='officematter/org_add_member.html'):
    org= get_object_or_404(Organization, pk=pk)    
    if request.method == "POST":
        form = OrganizationMemberForm(request.POST or None)
        if form.is_valid():
            org_member=  form.save(commit=False)
            org_member.OrgId = org
            org_member.save()
            return HttpResponseRedirect('/organization-list')
        else:
            return render(request, template_name, {'form_org': form})
    else:
        form = OrganizationMemberForm()     
        return render(request, template_name, {'form_org': form})


