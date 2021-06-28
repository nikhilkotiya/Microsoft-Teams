from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import HttpResponse 
import requests
from django.contrib.auth import authenticate, login
# Create your views here.
from .forms import RegistrationForm 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,force_text,DjangoUnicodeDecodeError 
from .utils import generator_token
from django.core.mail import EmailMessage
from django.conf import settings
def userdashboard(request):
    return render(request,'2ndtemp.html')
def send_action_email(user,request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('activate.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk )),
        'token': generator_token.make_token(user)
    })
    email=EmailMessage(subject=email_subject,body=email_body,
                from_email = settings.EMAIL_FROM_USER,
                to = [user.email]
                )
    email.send() 
def activate_user(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user and generator_token.check_token(user,token):
        user.is_email_verified = True
        user.save()
        messages.add_message(request,messages.SUCCESS,'Email Varified, Now you can login')
        return redirect(reversed('login'))

    return render(request,'activate-failed.html',{"user":user})

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.POST.get("form_one"):
        if not User.objects.filter(email=request.POST["email"]).exists():
            if request.POST["password"]==request.POST["rpassword"]:
                print(request.POST["password"])
                if (len(request.POST["password"]) > 7):
                    data=User()
                    data.password=make_password(request.POST["password"])
                    print(data.password)
                    data.first_name=request.POST["first_name"]
                    data.last_name=request.POST["last_name"]
                    data.username=request.POST["username"]
                    data.email = request.POST["email"]
                    print(data.email)
                    data.save()
                    send_action_email(data,request)
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
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6LfNIlcbAAAAAAcecCz5uoDbN6kPgJal0dd6W2Fk"
        cap_data ={"secret":cap_secret,"response":captcha_token}
        cap_server_response = requests.post(url=cap_url,data=cap_data)
        print(cap_server_response.text)

        result = cap_server_response.json()
        if result['success']==False:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return render(request,"index.html")
        user = authenticate(request,username=email, password=password)

        if not user.is_email_verified:
            messages.error(request, 'Email is not verified')
            return render(request,"index.html")
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

def about(request):
    return  HttpResponse("About page")
def send_email_to_user(otp,email):
    import smtplib
    con = smtplib.SMTP("smtp.gmail.com",587)
    con.ehlo()
    con.starttls()
    admin_email = "email"
    admin_password = "password"
    con.login(admin_email,admin_password)
    msg = "Otp is "+str(otp)
    con.sendmail("email",email,"Subject:Password Reset \n\n"+msg)

def send_warning_email(email):
    import smtplib
    con = smtplib.SMTP("smtp.gmail.com",587)
    con.ehlo()
    con.starttls()
    admin_email = "your email"
    admin_password = "your password"
    con.login(admin_email,admin_password)
    msg = "Some One is Trying To Login With Your Account !!"
    con.sendmail(admin_email,email,"Subject:Login Warning \n\n"+msg)