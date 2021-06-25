from django.urls import path,include
from . import views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # <--
urlpatterns = [
    path('home/' ,views.userdashboard,name = "home"),
    path('login/',views.index,name='index'),
    path('logout/',views.ulogout,name= "ulogout"),
    path('activate_user/<uidb64>/<token>',views.activate_user,name='activate'),
]