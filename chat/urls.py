from django.urls import path
from . import views

urlpatterns=[
    path("videocall/inside/<str:url>",views.mian_view,name="main_view"),
    path('text',views.text,name="text"),
    # path('send_mail/', views.sendMail, name='send_mail')
    path("",views.mian_view,name="main_view"),
    path("group/",views.index)
]