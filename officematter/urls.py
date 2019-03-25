
from django.contrib import admin
# from django.urls import path
from django.conf.urls import url

from officematter import views 
app_name="office-master"

urlpatterns = [   
    url(r'^$',views.index,name='index'),
    url(r'^about$',views.about,name='about'),    
    url(r'^topic$',views.topicPage,name='topic'),  
    url(r'^topic-from-api$',views.topicPageGetFromAPI_V2,name='topic-from-api'),
    url(r'^web-page$',views.Web_Page,name='web-page'),       
    url(r'^register$',views.register_view,name='register'),       
    url(r'^login$',views.login_view,name='login') ,       
    url(r'^logout$',views.user_logout,name='logout'),        
    url(r'^api/v1/users$',views.get_list_users,name='api/v1/users'), 
    url(r'^api/v2/topics$',views.restAPI_Topics,name='api/v2/topics'), 
    url(r'^users$',views.User_views,name='users'),
    url(r'^topic-create$',views.topic_create_view,name='topic-create'),

]
