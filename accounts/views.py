from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from feed.models import * 
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
import json


User = get_user_model()


def register(request):
	if(request.method == 'POST'):
		form = UserRegisterForm(request.POST)
		email = request.POST['email']
		if (email.endswith('nitw.ac.in') == False):
			messages.error(request,'Please enter a NITW email!')
			return render(request, 'accounts/register.html', {'form':form})
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			user = User.objects.get(username = username)
			name = form.cleaned_data.get('name')
			branch = form.cleaned_data.get('branch')
			year = form.cleaned_data.get('year')
			profile = Profile(user = user, name = name, branch=branch, year=year);
			profile.save()
			messages.success(request, f'Account created for {username}. Please login to proceed!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_edit(request):
	username = request.user.username
	if(request.method == 'POST'):
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile', request.user.username)

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	user = request.user
	profileuser = User.objects.get(username=username)
	p = profileuser.profile
	u = p.user
	user_posts = Post.objects.filter(author=profileuser).order_by('-date_posted')
	

	context = {
		'u' : u,
		'u_form': u_form,
		'p_form': p_form,
		'user_posts' : user_posts,
		'user' : user,
		'profileuser' : profileuser,
	}
	return render(request, 'accounts/profile_edit.html', context)

@login_required
def search_users(request):
	query = request.GET.get('q')
	object_list = User.objects.filter(username__icontains=query)
	context ={
		'users': object_list,
		'randusers' : User.objects.order_by('?')[:5],
	}
	return render(request, "accounts/search_users.html", context)


@login_required
def profile(request, username):
	user = request.user
	profileuser = User.objects.get(username=username)
	p = profileuser.profile
	u = p.user
	user_posts = Post.objects.filter(author=profileuser).order_by('-date_posted')
	projects = Project.objects.filter(author=profileuser)
	context = {
		'u' : u,
		'user_posts' : user_posts,
		'user' : user,
		'profileuser' : profileuser,
		'projects' : projects,
	}
	return render(request, 'accounts/profile.html', context)



