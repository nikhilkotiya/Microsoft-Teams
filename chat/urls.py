from django.urls import path
from . import views

urlpatterns=[
    path("",views.mian_view,name="main_view"),
    path('send_mail/', views.sendMail, name='send_mail')
]