#/chat/username

from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
	path('', views.AllChats, name='all-chats'),
    path('<str:username>/', views.Conversation, name='conversation'), 
]
