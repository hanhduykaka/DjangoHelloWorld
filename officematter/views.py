from django.shortcuts import render
from officematter.models import Topic, WebPage
from officematter.form import FormRegister
from officematter.models import Clients
# Create your views here.


def index(request):
    return render(request, "officematter/index.html")


def about(request):
    return render(request, "officematter/about.html")


def topicPage(request):
    topiclist = Topic.objects.all().order_by("top_name")
    return render(request, "officematter/topic.html",context= {'topic':topiclist})

def Web_Page(request):
    pagelist = WebPage.objects.all().order_by("name")
    return render(request, "officematter/webpage.html",context= {'pagelist':pagelist})

def register_view(request):  
    form = FormRegister()
    if request.method=='POST':
        form=FormRegister(request.POST,Clients)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['confirm']:
            request.POST._mutable = True
            post = form.save(commit=False)
            post.email=form.cleaned_data['email']
            post.username = form.cleaned_data['username']
            post.password = form.cleaned_data['password']
            post.save()
            print("đã insert dư liệu")
        # elif form.cleaned_data['password'] != form.cleaned_data['confirm']:
        #     form.add_error('confirm','the password do not match')
        #     print('pass word vs confirm password are not the same')

    return render(request, "officematter/register.html",{'form':form})
