from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.models import User
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import json

# import random

# items = Profile.objects.all()
# # change 3 to how many random items you want
# #if items.count() >= 5:
# #	randusers = random.sample(list(items), 5) REASON FOR NOT USING: this causes problems
# # in creating new columns in db

# # if you want only a single random item
# #random_item = random.choice(items)


# #uses cbv
# def home(request):
# 	context = {
#         'posts': Post.objects.all(),
#         'randusers' : User.objects.order_by('?')[:5],
#     }
# 	return render(request, 'feed/home.html', context)

class PostListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'feed/home.html'
	context_object_name = 'posts'
	ordering = '-date_posted'
	paginate_by = 4

	def get_context_data(self, **kwargs):
		context = super(PostListView, self).get_context_data(**kwargs)
		context['randusers'] = User.objects.order_by('?')[:5]
		return context


class PostDetailView(DetailView):
	model = Post
	context_object_name = 'post'
	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)

		reacted_by = get_object_or_404(Post, id=self.kwargs['pk'])
		context['upvotes'] = reacted_by.number_of_upvotes()
		context['downvotes'] = reacted_by.number_of_downvotes()
		context['comments'] = Comment.objects.filter(post=reacted_by)
		# context['post_is_liked'] = liked
		context['randusers'] = User.objects.order_by('?')[:5]
		return context

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content', 'image', 'anonymous']

	def get_context_data(self, **kwargs):
		context = super(PostCreateView, self).get_context_data(**kwargs)
		context['randusers'] = User.objects.order_by('?')[:5]
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content', 'image', 'anonymous']

	def get_context_data(self, **kwargs):
		context = super(PostUpdateView, self).get_context_data(**kwargs)
		context['randusers'] = User.objects.order_by('?')[:5]
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	context_object_name = 'post'
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = super(PostDeleteView, self).get_context_data(**kwargs)
		context['randusers'] = User.objects.order_by('?')[:5]
		return context

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



def PostUpvote(request, pk):
    data = json.loads(request.body.decode("utf-8"))
    id = data['post_id']
    only_check = data['only_check']
    post = get_object_or_404(Post, id=id)
    number_of_upvotes = 0
    if only_check == 1:
    	number_of_upvotes = post.number_of_upvotes()
    else:
	    if post.upvote.filter(id=request.user.id).exists():
	        post.upvote.remove(request.user)
	    else:
	        post.upvote.add(request.user)
	        if post.downvote.filter(id=request.user.id).exists():
	        	post.downvote.remove(request.user)
	    number_of_upvotes = post.number_of_upvotes()
    
    return HttpResponse(number_of_upvotes)


def PostDownvote(request, pk):
    data = json.loads(request.body.decode("utf-8"))
    id = data['post_id']
    only_check = data['only_check']
    post = get_object_or_404(Post, id=id)
    number_of_downvotes = 0
    if only_check == 1:
    	number_of_downvotes = post.number_of_downvotes()
    else:
	    if post.downvote.filter(id=request.user.id).exists():
	        post.downvote.remove(request.user)
	    else:
	        post.downvote.add(request.user)
	        if post.upvote.filter(id=request.user.id).exists():
	        	post.upvote.remove(request.user)
	    number_of_downvotes = post.number_of_downvotes()
    return HttpResponse(number_of_downvotes)

@login_required
def comment_create(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('post_comment')
        com_user = request.user

        if not content:
        	return redirect('post-detail', pk)

    Comment.objects.create(post=post, author=com_user, content=content)
    return redirect('post-detail', pk)


def project_upload(request):
	if request.method=='POST':
		title = request.POST.get('title')
		content = request.POST.get('content')
		link = request.POST.get('link')
		img = request.FILES['img']
		author = request.user
		project = Project(author=author, title=title, content=content, link=link, image=img)
		project.save()
		return redirect('profile', author.username)
	return render(request,'feed/project_upload.html')