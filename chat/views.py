from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q

def unionUser(q1,q2):
	user_list = []
	for obj in q1:
		user_list.append(obj.sender)

	for obj in q2:
		user_list.append(obj.receiver)

	user_list = set(user_list)
	return user_list

def AllChats(request):
	user = request.user
	#messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('timestamp')
	q1 = Message.objects.filter(receiver=user).only('sender')
	q2 = Message.objects.filter(sender=user).only('receiver')

	user_list = unionUser(q1,q2)
	context = {
		'user_list' : user_list,
	}

	return render(request, 'chat/allchats.html',context)


def Conversation(request, username):
	user = request.user
	user2 = User.objects.get(username=username)
	messages = Message.objects.filter(Q(sender=user,receiver=user2) | Q(receiver=user,sender=user2)).order_by('timestamp')
	
	context = {
		'messages' : messages,
		'user' : user,
	}

	return render(request, 'chat/conversation.html',context)
