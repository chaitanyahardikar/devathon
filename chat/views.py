from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import json

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
	if request.method == 'POST':
		print("it is a post request")
		data = json.loads(request.body.decode("utf-8"))
		curr_msg = data['msg']
		fetch_only = data['fetch_only']

		if fetch_only == 0:
			new_msg = Message(sender=user, receiver=user2, content=curr_msg)
			new_msg.save();
		messages = list(Message.objects.filter(Q(sender=user,receiver=user2) | Q(receiver=user,sender=user2)).order_by('timestamp').values())

		messages_with_username = []
		for message in messages:
			msg = {}
			msg['content'] = message['content']
			msg['sender'] = User.objects.filter(id = message['sender_id'])[0].username
			msg['receiver'] = User.objects.filter(id = message['receiver_id'])[0].username
			msg['timestamp'] = message['timestamp']
			temp = str(message['timestamp'])
			# 2021-09-18T17:49:30.180Z
			msg_time = temp[11:16]
			msg['msg_time'] = msg_time

			messages_with_username.append(msg)
		return JsonResponse(messages_with_username, safe=False)  

	messages = Message.objects.filter(Q(sender=user,receiver=user2) | Q(receiver=user,sender=user2)).order_by('timestamp')
	
	context = {
		'messages' : messages,
		'user' : user,
	}

	return render(request, 'chat/conversation.html',context)

