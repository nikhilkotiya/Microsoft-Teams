from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
# Create your views here.
def mian_view(request):
    if request.user.is_authenticated:
        context={}
        return render(request,'chat/main.html',context=context)
    else:
        return redirect('index')
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
def sendMail(request):
    if request.method == 'POST':
        sender = settings.EMAIL_HOST_USER
        receiver = request.POST['receiver']
        subject = request.POST['sub']
        content = request.POST['content']

        mail = send_mail(subject, content, sender, [receiver])
        if mail:
            messages.success(request, 'Email has been sent.')
            return redirect('main_view')
        else:
            return HttpResponse('message not sent')
    else:
        return render(request,'chat/home.html')