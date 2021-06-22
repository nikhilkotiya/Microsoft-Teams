from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import HttpResponse 
from django.contrib.auth import authenticate, login
# Create your views here.
from .auth import EmailBackend
from .forms import RegistrationForm 
def userdashboard(request):
    return render(request,'2ndtemp.html')
 
def index(request):
    if request.user.is_authenticated:
        print(request.user)
        print(request.email)
        return redirect('home')
    if request.POST.get("form_one"):
        if not User.objects.filter(email=request.POST["email"]).exists():
            if request.POST["password"]==request.POST["rpassword"]:
                if (len(request.POST["password"]) > 7):
                    data=User()
                    data.password=make_password(request.POST["password"])
                    data.first_name=request.POST["first_name"]
                    data.last_name=request.POST["last_name"]
                    data.username=request.POST["username"]
                    data.email = request.POST["email"]
                    data.save()
                    print("user saved")
                    messages.success(request, 'Account crated succesfully.')
                    return render(request,"index.html")
                else:
                    context="Length must be greter then 8"
                    return render(request,"index.html",{'errorP':context})

            else:
                context="Password confirmation doesn't match"
                print("wrong password")
                return render(request,"index.html",{'errorPC':context})

        else:
            context="Email Already Exist"
            return render(request,"index.html",{'errorE':context})              
    elif request.POST.get("form_two"):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,username=email, password=password)
        print(user)

        if user is not None:
            login(request, user)
            print('welcome')
            return redirect('home')	
        else:
            print('wrong input ')
            context="Wrong Email or Password"
            return render(request,"index.html",{"invalid":context})
    else:
        return render(request,"index.html")


def ulogout(request):
    print("log out")
    logout(request)
    return redirect('index')


def profile(request):
    f=request.user.first_name
    l=request.user.last_name
    e=request.user.username
    print(f)
    print(l)
    print(e)
    return render(request,'profile.html' ,{'f':f,'l':l,'e':e})


def about(request):
    return  HttpResponse("About page")


def test(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        # data.password=request.POST["password"]
        # data.first_name=request.POST["first_name"]
        # data.last_name=request.POST["last_name"]
        # data.username=request.POST["username"]
        # data.email = request.POST["email"]
        # data.is_active = True
        # data.is_superuser=False
        # data.is_admin=False
        # print(data.first_name)
        # print(data.last_name)
        # print(data.email)
        # print(data.password)
        # print(data.username)
        # print(data.is_active)
        # print(data.is_superuser)
        # print(data.is_admin)
        if form.is_valid():
            form.save()
            print("user saved")
        else:
            print("Error")
        form=RegistrationForm()
        return HttpResponse(form.errors) 
    else:
        form=RegistrationForm()
        return render(request,'test.html',{'form':form})


def profile(request):
    f=request.user.first_name
    l=request.user.last_name
    e=request.user.email
    print(e)
    return render(request,'profile.html' ,{'f':f,'l':l,'e':e})