from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
# Create your views here.
def mian_view(request):
    if request.user.is_authenticated:
        context={}
        return render(request,'chat/main.html',context=context)
    else:
        return redirect('index')
    