from django.urls import path,include
from . import views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # <--
urlpatterns = [
    path('home/' ,views.userdashboard,name = "home"),
    path('',views.index,name='index'),
    path('logout',views.ulogout,name= "ulogout"),
    path('home/profile/',views.profile,name="profile"),
    path('home/about/',views.about,name="about"),
    path('accounts/', include('allauth.urls')),
    path('home/profile/',views.profile,name="profile"),
    path('test/',views.test,name='test')
]