from django.shortcuts import render
from officematter.models import Topic,WebPage

# Create your views here.

def index(request):
    return render(request,"officematter/index.html")

def about(request):
    return render(request,"officematter/about.html")

def topicPage(request):
    topiclist = Topic.objects.all().order_by("top_name")
    return render(request,"officematter/topic.html")