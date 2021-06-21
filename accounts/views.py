import base64
import mimetypes
import os
import os.path
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMessage
from email.mime.text import MIMEText
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.views import generic
from googleapiclient import errors, discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from  .forms import SignupForm
from .models import User
def home(request):
    return render(request,"landingPage.html")

def is_active_check(user):
    return user.is_active


@login_required
@user_passes_test(is_active_check)
@permission_required('users.view_user', raise_exception=True)
def login_next(request):
    return HttpResponse("Hello, world. This is a log in page")
class SignUpView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token
from django.core.mail import send_mail

# def signup(request):
#     User = get_user_model()
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             if User.objects.filter(email__iexact=email).count() == 1:
#                 user = form.save(commit=False)
#                 user.is_active = False
#                 user.save()
#                 current_site = get_current_site(request)
#                 mail_subject = 'Activate your account.'
#                 message = render_to_string('email_template.html', {
#                             'user': user,
#                             'domain': current_site.domain,
#                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                             'token': account_activation_token.make_token(user),
#                         })
#                 to_email = form.cleaned_data.get('email')
#                 send_mail(mail_subject, message, 'youremail', [to_email])
#                 return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignupForm()
#     return render(request, 'regform.html', {'form': form})

# def activate(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')

def create_message(sender, to, subject, message_text):
    """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
  Returns:
    An object containing a base64url encoded email object.
  """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def create_message_with_attachment(sender, to, subject, message_text, file):
    """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.
  Returns:
    An object containing a base64url encoded email object.
  """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, message):
    """Send an email message.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
  Returns:
    Sent Message.
  """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            user = User.objects.get(email=data)
            if user.exists():
                subject = "Password Reset Requested"
                email_template_name = "registration/password_reset_email.txt"
                c = {
                    "email": user.email,
                    'domain': '65.1.118.29',
                    'site_name': 'alumnibees.com',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                message_text = render_to_string(email_template_name, c)
                message = create_message('vinit.kumar@alumnibees.com', user.email, subject, message_text)
                try:
                    send_message(service_obj, 'me', message)
                except errors:
                    return HttpResponse('Error')
                return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset_form.html",
                  context={"password_reset_form": password_reset_form})


# unused functions
def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email, password=password)
        print(user)

        if user is not None:
            auth_login(request, user)
            print('welcome')
            return redirect('home')	
        else:
            return HttpResponse("You are not a user, Please signup for becoming a user.")

    else:
        return render(request,"registration/login.html") 

@login_required
def ulogout(request):
    print("log out")
    logout(request)
    return redirect('/')

def email_check(user):
    return user.email.endswith('@gmail.com')


# def signup(request):
#     if request.method=="POST":
#         if not User.objects.filter(email=request.POST["email"]).exists():
#             if request.POST["password"]==request.POST["rpassword"]:
#                 if (len(request.POST["password"]) > 7):
#                     data=User()
#                     data.password=make_password(request.POST["password"])
#                     data.first_name=request.POST["first_name"]
#                     data.last_name=request.POST["last_name"]
#                     data.email = request.POST["email"]
#                     data.is_active = True
#                     print("user saved")
#                     data.save()
#                     return render(request,"login.html")
#                 else:
#                     context="Length must be greter then 8"
#                     return render(request,"login.html",{'errorP':context})

#             else:
#                 context="Password confirmation doesn't match"
#                 print("wrong password")
#                 return render(request,"login.html",{'errorPC':context})
#         else:
#             context="Email Already Exist"
#             return render(request,"login.html",{'errorE':context})             

# def login(request):
#     if request.method=="POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request,email=email, password=password)
#         print(user)

#         if user is not None:
#             auth_login(request, user)
#             print('welcome')
#             return redirect('home')	
#         else:
#             print('wrong input ')
#             context="Wrong Email or Password"
#             return render(request,"login.html",{"invalid":context})
#     else:
#         return render(request,"login.html")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            })            
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')