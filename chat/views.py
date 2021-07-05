from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.conf import settings
import speech_recognition as sr

from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.
def mian_view(request):
    if request.user.is_authenticated:
        context={}
        return render(request,'chat/main.html',context=context)
    else:
        return redirect('index')
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def text(request):
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")
        file = request.POST["file"]
        print(file)
        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
        return render(request,'index-FINISHED.html', {"transcript":transcript})
    return render(request,'index-FINISHED.html', {"transcript":transcript})