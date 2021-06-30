from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import Message
# from users.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

@login_required
def Inbox(request):
	messages = Message.get_messages(user=request.user)
	active_direct = None
	directs = None
	if messages:
		message = messages[0]
		active_direct = message['user'].email
		directs = Message.objects.filter(user=request.user, recipient=message['user'])
		directs.update(is_read=True)
		for message in messages:
			if message['user'].email == active_direct:
				message['unread'] = 0
	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
		}
	template = loader.get_template('direct/direct.html')
	return HttpResponse(template.render(context, request))

@login_required
def UserSearch(request):
    if request.method=="POST":
        user=User.objects.all()
        context = {'users': user}
    else:
        query = request.GET.get("q")
        context = {}
        if query:
            users = User.objects.filter(Q(email__icontains=query))

            #Pagination
            paginator = Paginator(users, 20)
            page_number = request.GET.get('page')
            users_paginator = paginator.get_page(page_number)

            context = {
                    'users': users_paginator,
                }
    template = loader.get_template('direct/search_user.html')
    return HttpResponse(template.render(context, request))

@login_required
def Directs(request, email):
		from_user = request.user
		to_user_email = request.POST.get('to_user')
		body = request.POST.get('body')
		if request.method == 'POST':
			to_user = User.objects.get(email=to_user_email)
			Message.send_message(from_user, to_user, body)
			
		user = request.user
		messages = Message.get_messages(user=user)
		active_direct = email
		directs = Message.objects.filter(user=user, recipient__email=email)
		e=request.user.email
		o=User.objects.get(email=email)
		other = Message.objects.filter(user=o, recipient__email=e)
		directs.update(is_read=True)
		for message in messages:
			if message['user'].email == email:
				message['unread'] = 0

		context = {
			'directs': directs,
			'messages': messages,
			'active_direct':active_direct,
		}

		template = loader.get_template('direct/private.html')

		return HttpResponse(template.render(context, request))


@login_required
def NewConversation(request,email):
	from_user = request.user
	body = ''
	try:
		to_user = User.objects.get(email=email)
	except Exception as e:
		return redirect('usersearch')
	if from_user != to_user:
		Message.send_message(from_user, to_user, body)
	return redirect('inbox')

@login_required
def SendDirect(request,email):
	if request.method=="POST":
		from_user = request.user
		to_user_email = request.POST.get('to_user')
		body = request.POST.get('body')
		if request.method == 'POST':
			to_user = User.objects.get(email=to_user_email)
			Message.send_message(from_user, to_user, body)
			return redirect('directs')
		else:
			HttpResponseBadRequest()
def checkDirects(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()
	return {'directs_count':directs_count}