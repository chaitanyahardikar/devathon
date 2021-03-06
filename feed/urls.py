from django.urls import path
from . import views
from accounts import views as accounts_views

# app_name = "feed" 

urlpatterns = [
    path('', views.PostListView.as_view(), name='feed-home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('profile/<str:username>', accounts_views.profile, name='profile'),
    path('post-upvote/<int:pk>', views.PostUpvote, name='post-upvote'),
    path('post-downvote/<int:pk>', views.PostDownvote, name='post-downvote'),
    path('comment/<int:pk>', views.comment_create, name='comment'),
    path('project-upload/', views.project_upload, name='project_upload'),
]
