from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.
def mian_view(request):
    if request.user.is_authenticated:
        context={}
        return render(request,'chat/main.html',context=context)
    else:
        return redirect('index')