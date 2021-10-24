
from django.contrib import admin
from django.urls import path,include
from  django.conf import settings
from django.conf.urls.static import static
from blog import views
from django.conf.urls import url
from django.views.static import serve

app_name='blog'

urlpatterns = [
    path('',views.all_blogs, name='all_blogs'),
    path('<int:blog_id>/view',views.detail, name='detail'),
    path('<int:blog_id>/',views.post_comment,name='post_comment'),
    path('all',views.list_blog,name='list_blog'),
    path ('category/<str:category>',views.category,name='category'),
]
